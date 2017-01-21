#
# -*- coding: utf-8 -*-
####################
# pyGPG Config
####################
# File:       config.py
#
#             Python configuration and options class for
#             an Interface access to gnupg
#
# Copyright:
#             (c) 2012-2017 Brian Dolbec
#             Distributed under the terms of the BSD license
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's config's.'''

import re


class GPGConfig(object):
    '''holds all options and configuration data
    for running the GnuPG class'''

    defaults = {
        'clearsign': '--clearsign',
        'decrypt': '--decrypt',
        'delete-keys': '--delete-keys',
        'detach-sign': '--detach-sign',
        'dump-options': '--dump-options',
        'fingerprint': '--fingerprint',
        'gpg_command': '/usr/bin/gpg',
        'import': '--import',
        'list-key': '--list-key',
        'list-keys': '--list-keys',
        'list-secret-keys': '--list-secret-keys',
        'no-tty': '--no-tty',
        'recv-keys': '--recv-keys',
        'refresh-keys': '--refresh-keys',
        'search-keys': '--search-keys',
        'send-keys': '--send-keys',
        'sign': '--sign',
        'verify': '--verify',
        'version': '--version',
        # defaults added to each gpg process run
        'gpg_defaults': ['--display-charset', 'utf-8', '--status-fd', '2',
            '--no-tty'],
        'only_usable': False,
        'refetch': False,
        'tasks': {
            'clearsign': [],
            'decrypt': [],
            'delete-keys': [],
            'detach-sign': [],
            'dump-options': [],
            'fingerprint': [],
            'import': [],
            'list-keys': [],
            'list-key': [],
            'list-secret-keys': [],
            'recv-keys': [],
            'refresh-keys': ['--with-colons'],
            'search-keys': [],
            'send-keys': [],
            'sign': [],
            'verify': [],
            'version': [],
        },
        'trust-models': ['always', 'auto', 'classic', 'direct', 'pgp'],
    }


    def __init__(self):
        '''Class init function'''
        self.options = {
            'tasks': {}
        }
        self.unsupported = set()
        self.sub_re = r'.*\%(.*)'
        self.type_re = re.compile(r'(type)|[< >\']')

    def __getitem__(self, key):
        return self._get_(key)


    def _get_(self, key, subkey=None):
        '''Class specific private get function'''
        if (key in self.options and not self.options[key] is None):
            if subkey:
                if subkey in self.options[key]:
                    return self._sub_(self.options[key][subkey])
                elif subkey in self.defaults[key]:
                    return self._sub_(self.defaults[key][subkey])
                else:
                    return None
            return self._sub_(self.options[key]) or \
                self._sub_(self.defaults[key])
        elif key in self.defaults:
            if subkey:
                if subkey in self.defaults[key]:
                    return self._sub_(self.defaults[key][subkey])
                else:
                    return None
            return self._sub_(self.defaults[key])
        print("NOT found", key, subkey)
        return None


    def get_key(self, key, subkey=None):
        '''Returns a specified key or subkey value

        @param key: string config default or config options key identifier
        @param subkey: string (optional) config key's subkey identifier
        @rtype specific to the key or subkey's value being retrieved
        '''
        return self._get_(key, subkey)


    def get_defaults(self):
        '''Returns a dictionary of the default settings

        @rtype dict
        '''
        return self.defaults.copy()


    def sign_modes(self, gpg_options=None):
        '''Returns the list of supported signing types.

        @param gpg_options: list of gpg options such as those returned by
            GnuPG.dump_options(). If passed in, it will do a set intersection
            of the supported signing modes and gpg_options
        @rtype list: of supported signing options
            '''
        supported = ["clearsign", "sign", "detach-sign"]
        if gpg_options:
            return list(set(supported).intersection(gpg_options))
        return supported


    def _sub_(self, data):
        '''Return command that performs the
        %(variable)s substitution at time of the call.
        This allows for changing values dynamically.
        This functions determines the data type and calls the
        appropriate _sub_*().

        @param data: unknown, one of string, dict, list, tuple
        @return: data of the same type
        '''
        data_type = type(data)
        data_type = re.sub(self.type_re, '', str(data_type)).replace('class', '')
        if data_type not in ['dict', 'list', 'str', 'tuple']:
            return data
        func = getattr(self, '_sub_%s' % data_type)
        return func(data)


    def _sub_dict(self, data):
        '''Return command that performs the
        %(variable)s substitution at time of the call.
        This allows for changing values dynamically

        @param data: dictionary
        @return: dictionary
        '''
        new = {}
        for key, value in list(data.items()):
            new[key] = self._sub_(value)
        return new


    def _sub_list(self, data):
        '''Return command that performs the
        %(variable)s substitution at time of the call.
        This allows for changing values dynamically

        @param data: list
        @return: list
        '''
        new = []
        for member in data:
            new.append(self._sub_(member))
        return new

    def _sub_str(self, data):
        '''Return command that performs the
        %(variable)s substitution at time of the call.
        This allows for changing values dynamically

        @param data: string
        @return: string
        '''
        data2 = None
        if re.match(self.sub_re, data):
            try:
                data2 = data % self.options
            except KeyError:
                pass
        if re.match(self.sub_re, data):
            try:
                data2 = data % self.defaults
            except KeyError:
                pass
        return data2 or data


    def _sub_tuple(self, data):
        '''Return command that performs the
        %(variable)s substitution at time of the call.
        This allows for changing values dynamically

        @param data: tuple
        @return: tuple
        '''
        new = []
        for member in data:
            new.append(self._sub_(member))
        return tuple(new)


