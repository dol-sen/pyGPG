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


import sys
if sys.version_info[0] >= 3:
    _str = str
    _unicode = str
else:
    _str = basestring
    _unicode = unicode


from pyGPG.status import Status
from pyGPG.legend import FINGERPRINT_CLASSES


def encode(text, enc="UTF-8"):
    """py2, py3 compatibility function"""
    if hasattr(text, 'decode'):
        return text.decode(enc)
    return str(text)


class GPGResult(object):
    '''GnuPG process result handler'''


    def __init__(self, gpg, results, extract_stdout=False):
        '''Class init function'''
        self.gpg = gpg
        self.output = results[0]
        self.stderr_out = results[1]
        self.decode_errors = []
        if isinstance(self.output, bytes):
            try:
                self.output = self.output.decode('UTF-8')
                self.stderr_out = self.stderr_out.decode('UTF-8')
            except UnicodeDecodeError:
                self.decode_errors.append("pyGPG.output(): Error decoding gpg output with utf-8")
                self.decode_errors.append(self.output)
                self.decode_errors.append(self.stderr_out)
                self.status = Status()
                self.failed = True
                return
        self.stderr_out = _unicode(self.stderr_out)
        self.stderr_out = self.stderr_out.split('\n')
        self.status = Status()
        if extract_stdout:
            self.messages = self.status.extract_output(self.output)
        else:
            self.messages = self.status.extract_data(self.stderr_out)
        # set failed default, for use by consumer apps
        self.failed = False


    @property
    def verified(self):
        '''Checks the output status data for good or valid signatures

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
        data = self.get_data(fields)
        results = []
        for item in data:
            if item[2] is not '':
                results.append(item)
        if not results:
            return self.fingerprint
        return results


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
        fields = ['username', 'user_ID']
        r = self.get_data(fields)
        results = []
        for item in r:
            if item[2]:
                results.append(item)
        return results


    @property
    def fingerprint(self):
        '''Looks for fingerprint status data types in the status messages

        @rtype list: of matching legend class instances found
        '''
        fields = ['fingerprint']
        data = self.get_data(fields, FINGERPRINT_CLASSES)
        results = []
        for item in data:
            if item[2]:
                results.append(item)
        return results


    @property
    def returncode(self):
        '''The return code of the gpg process that was run

        @rtype int
        '''
        if self.gpg:
            return self.gpg.returncode or -1
        return -1

    @property
    def no_pubkey(self):
        '''Checks the output status data for a NO_PUBKEY result.

        This indicates it failed to find the correct signature
        in the keyring

        @rtype tuple: (bool, keyid)
        '''
        pub_key = self.get_data(status_type=['NO_PUBKEY'])
        if pub_key:
            return (True, pub_key[0].long_keyid)
        return (False, None)


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
        if isinstance(param, _str):
            param = [param]
        # else assume it is an iterable, if not it will error
        return [encode(i) for i in param]
