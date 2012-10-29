#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# pyGPG Config
#################################################################################
# File:       config.py
#
#             Python configuration and options class for
#             an Interface access to gnupg
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's config's.'''



class GPGConfig(object):
    '''holds all options and configuration data
    for running the GnuPG class'''

    def __init__(self):
        self._defaults = {
            'gpg_command': '/usr/bin/gpg',
            'decrypt': '--decrypt',
            'verify': '--verify',
            'sign': '--sign',
            'clearsign': '--clearsign',
            'detach-sign': '--detach-sign',
            'dump-options': '--dump-options',
            'list-keys': '--list-keys',
            'list-secret-keys': '--list-secret-keys',
            'no-tty': '--no-tty',
            'version': '--version',
            # defaults added to each gpg process run
            'gpg_defaults': '--status-fd 2 --no-tty',
            'only_usable': False,
            'refetch': False,
        }
        self.options = {
        }
        self.task_options = {
            'decrypt': '',
            'verify': '',
            'sign': '',
            'clearsign': '',
            'detach-sign': '',
            'dump-options': '',
            'list-keys': '--attribute-fd 2',
            'list-secret-keys': '--attribute-fd 2',
            'version': '',
        }
        self.unsupported = set()


    def __getitem__(self, key):
        return self._get_(key)


    def _get_(self, key):
        if (key in self.options
            and not self.options[key] is None):
            return self.options[key]
        if key in self._defaults:
            return self._defaults[key]
        return None


    def get_defaults(self):
        '''Returns a dictionary of the default settings
        '''
        return self._defaults.copy()


    def sign_modes(self, gpg_options=None):
        '''Returns the list of supported signing types
        @param gpg_options: list of gpg options such as those returned by
            GnuPG.dump_options(). If passed in, it will do a set intersection
            of the supported signing modes and gpg_options
        @rtype list: of supported signing options
            '''
        supported = ["clearsign", "sign", "detach-sign"]
        if gpg_options:
            return list(set(supported).intersection(set(gpg_options)))
        return supported

