#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# pyGPG GPG handler
#################################################################################
# File:       gnupg.py
#
#             Python Interface access to gnupg
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles running gnupg.'''

from __future__ import with_statement

import os
import copy
from subprocess import Popen, PIPE

from pygpg.output import GPGResult


class GPG(object):
    '''Subprocess gnupg handler class'''

    def __init__(self, config):
        '''
        @param config: GPGConfig config instance
        '''
        self.config = config
        self._gpg_version = None
        self._gpg_options = None
        self.history = []
        self.env = copy.copy(os.environ)


    def runGPG(self, action=None, gpg_input=None, filepath=None):
        '''Creates, opens and runs the subprocess object
        @rtype GnuPGResult object
        '''
        results = ('', '') # null
        gpg = None
        if not action:
            return None
        args = [self.config['gpg_command']]
        args.extend(self.config['gpg_defaults'])
        task_opts = self.config.get('tasks', action)
        if task_opts:
            args.extend(task_opts)
        args.append(self.config[action])
        args = [x for x in args if x != '']
        if gpg_input is not None:
            # history is only for initial debugging
            self.history.append("Running gpg with: '%s'" % str(args))
            gpg = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                env=self.env)
            results = gpg.communicate(gpg_input)
        elif filepath is not None:
            args.extend(['-o',filepath])
            # history is only for initial debugging
            self.history.append("Running gpg with: '%s'" % str(args))
            # need to set stdin to /dev/null
            gpg = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                env=self.env)
            results = gpg.communicate('')
        return GPGResult(gpg, results)


    def decrypt(self, gpg_input=None, filepath=None):
        '''Decrypts the gpg_input block passed in
        or the file found at filepath.

        @rtype GnuPGResult object
        '''
        return self.runGPG('decrypt', gpg_input, filepath)


    def verify(self, gpg_input=None, filepath=None):
        return self.runGPG('verify', gpg_input, filepath)


    def sign(self, mode, gpg_input=None, filepath=None):
        if mode not in self.config.sign_modes():
            return GPGResult(None, '', 'pyGPG: Error, no/unsupported signing'
                'mode passed in: %s\n' % mode)
        return self.runGPG(mode, gpg_input, filepath)


    @property
    def options(self):
        '''Runs 'gpg --dump-options' for a list of all available gpg options.
        config parameter only_usable: Boolean, When True will filter
            the returned list to only contain the options this class
            is capable of using.
        config parameter refetch: Boolean
        @rtype list: of options from gpg'''
        if not self._gpg_options or self.config['refetch']:
            self._gpg_options = self.runGPG('dump-options', '')
        opts = self._gpg_options.output.split("\n")
        if self.config['only_usable']:
            return list(set(opts.difference(self.config.unsupported)))
        return opts


    @property
    def version(self):
        '''Runs 'gpg --version'
        @param refetch: Boolean
        @rtype list: of options from gpg'''
        if (self._gpg_version is None) or self.config['refetch']:
            self._gpg_version = self.runGPG('version', '')
        return self._gpg_version.output.split("\n")

