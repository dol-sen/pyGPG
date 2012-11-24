#!/usr/bin/python
# -*- coding: utf-8 -*-
####################
# pyGPG GnuPGResult
####################
# File:       output.py
#
#             Python class for interpreting the results
#             of a gpg operation
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the BSD license
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
        '''Class init function'''
        self.gpg = gpg
        self.output = results[0]
        self.stderr_out = results[1].split('\n')
        self.status = Status()
        self.messages = self.status.extract_data(self.stderr_out)


    @property
    def verified(self):
        '''Checks the output status data for goog or valid signatures

        @rtype tuple: (bool: verification staus,
            trust: legend.TRUST_* class instance or 'Unknown')
        '''
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
        '''Looks for time status data types in the status messages

        @rtype list: of matching legend class instances found
        '''
        fields = ['timestamp', 'sig_timestamp', 'expire_timestamp', ]
        return self.get_data(fields)


    @property
    def keyid(self):
        '''Looks for keyid status data types in the status messages

        @rtype list: of matching legend class instances found
        '''
        fields = ['long_keyid', 'long_main_keyid']
        return self.get_data(fields)


    @property
    def keytype(self):
        '''Looks for keytype status data types in the status messages

        @rtype list: of matching legend class instances found
        '''
        fields = ['keytype']
        return self.get_data(fields)


    @property
    def username(self):
        '''Looks for username status data types in the status messages

        @rtype list: of matching legend class instances found
        '''
        fields = ['username']
        return self.get_data(fields)


    @property
    def fingerprint(self):
        '''Looks for fingerprint status data types in the status messages

        @rtype list: of matching legend class instances found
        '''
        fields = ['fingerprint']
        return self.get_data(fields)


    @property
    def returncode(self):
        '''The return code of the gpg process that was run

        @rtype int
        '''
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
        @rtype list: of (type name,field,data) tuples
        '''
        if status_type is None:
            status_type = [x.name for x in self.status.data]
        else:
            status_type = self._check_param_type(status_type)
        if fields is None:
            return [x for x in self.status.data if x.name in status_type]
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
