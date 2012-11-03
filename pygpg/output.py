#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# pyGPG GnuPGResult
#################################################################################
# File:       output.py
#
#             Python class for interpreting the results
#             of a gpg operation
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's gpg output.'''


from pygpg.status import Status


def encode(text, enc="UTF-8"):
    """py2, py3 compatibility function"""
    if hasattr(text, 'decode'):
        return text.decode(enc)
    return str(text)


class GPGResult(object):
    '''GnuPG process result handler'''

    def __init__(self, gpg, results):
        self.gpg = gpg
        self.output = results[0]
        self.stderr_out = results[1].split('\n')
        self.status = Status()
        self.messages = self.status.extract_data(self.stderr_out)


    @property
    def verified(self):
        good = ['GOODSIG', 'VALIDSIG', 'SIG_CREATED']
        trusts = ['TRUST_UNDEFINED', 'TRUST_NEVER', 'TRUST_MARGINAL',
            'TRUST_FULLY', 'TRUST_ULTIMATE']
        valid = self.get_data(status_type=good) != []
        trust = self.get_data(status_type=trusts)
        if len(trust):
            trust = trust[0]
        else:
            trust = 'Unknown'
        return (valid, trust)


    @property
    def time(self):
        fields = ['timestamp', 'sig_timestamp', 'expire_timestamp', ]
        return self.get_data(fields)


    @property
    def keyid(self):
        fields = ['long_keyid', 'long_main_keyid']
        return self.get_data(fields)


    @property
    def keytype(self):
        fields = ['keytype']
        return self.get_data(fields)


    @property
    def fingerprint(self):
        fields = ['fingerprint']
        return self.get_data(fields)


    @property
    def returncode(self):
        '''The return code of the gpg process that was run '''
        return self.gpg.returncode


    def get_fields(self, status_type=None):
        '''get a list of (type name,fields) tuples available from the gpg run

        @param staus_type: string or list of class name strings
            to search the data for
        @returns list: of fields with availble data
        '''
        if status_type is None:
            return [(x.name, x._fields) for x in self.status.data]
        status_type = self._check_param_type(status_type)
        return [(x.name, x._fields)
            for x in self.status.data if x.name in status_type]


    def get_data(self, fields=None, status_type=None):
        '''get a list of (type name,field,data) tuples available from the gpg run

        @param fields: string or list of field name strings to search for
        @param staus_type: string or list of class name strings to search for
        @returns list: of (type name,field,data) tuples
        '''
        if status_type is None:
            status_type = [x.name for x in self.status.data]
        else:
            status_type = self._check_param_type(status_type)
        if fields is None:
            fields = []
            for x in self.status.data:
                fields.extend(list(x._fields))
        else:
            fields = self._check_param_type(fields)

        results = []
        for x in self.status.data:
            if x.name in status_type:
                for f in x._fields:
                    if f in fields:
                        results.append((x.name, f, getattr(x, f)))
        return results


    @staticmethod
    def _check_param_type(param):
        """internal function that validates the repos parameter,
        converting a string to a list[string] if it is not already a list.
        produces and error message if it is any other type
        returns repos as list always"""
        if isinstance(param, basestring):
            param = [param]
        # else assume it is an iterable, if not it will error
        return [encode(i) for i in param]
