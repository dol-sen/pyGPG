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
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the BSD license
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's config's.'''



class GPGConfig(object):
    '''holds all options and configuration data
    for running the GnuPG class'''

    defaults = {
        'gpg_command': '/usr/bin/gpg2',
        'decrypt': '--decrypt',
        'verify': '--verify',
        'sign': '--sign',
        'clearsign': '--clearsign',
        'detach-sign': '--detach-sign',
        'dump-options': '--dump-options',
        'fingerprint': '--fingerprint',
        'list-key': '--list-key',
        'list-keys': '--list-keys',
        'list-secret-keys': '--list-secret-keys',
        'search-keys': '--search-keys',
        'no-tty': '--no-tty',
        'version': '--version',
        # defaults added to each gpg process run
        'gpg_defaults': ['--status-fd', '2', '--no-tty'],
        'only_usable': False,
        'refetch': False,
        'tasks': {
            'decrypt': [],
            'verify': [],
            'sign': [],
            'clearsign': [],
            'detach-sign': [],
            'dump-options': [],
            'fingerprint': [],
            'list-keys': ['--attribute-fd', '2'],
            'list-key': ['--attribute-fd', '2'],
            'list-secret-keys': ['--attribute-fd', '2'],
            'search-keys': [],
            'version': [],
        }
    }


    def __init__(self):
        '''Class init function'''
        self.options = {
            'tasks': None
        }
        self.unsupported = set()


    def __getitem__(self, key):
        return self._get_(key)


    def _get_(self, key, subkey=None):
        '''Class specific private get function'''
        if (key in self.options and not self.options[key] is None):
            if subkey:
                if subkey in self.options[key]:
                    return self.options[key][subkey]
                elif subkey in self.defaults[key]:
                    return self.defaults[key][subkey]
                else:
                    return 'foo-bar\'d subkey... options'
            return self.options[key] or self.defaults[key]
        elif key in self.defaults:
            if subkey:
                if subkey in self.defaults[key]:
                    return self.defaults[key][subkey]
                else:
                    return 'foo-bar\'d subkey... defaults'
            return self.defaults[key]
        return 'foo-bar\'d key'


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

