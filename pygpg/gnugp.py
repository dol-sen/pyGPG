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

from subprocess import Popen, PIPE



class GnuPG(object):
    '''Subprocess gnupg handler class'''

    def __init__(self, config):
        '''
        @param config: GPGConfig config instance
        '''
        self.config = config
        self._gpg_version = None


    def _process_gpg(self, action, message, filepath):
        '''Creates and opens the subprocess object
        @rtype GnuPGResult object
        '''
        results = ('', '') # null
        if message:
            args = [self.config['gpg_command'],
                    self.config[action],
                    self.config.get_options()
                ]
            gpg = Popen(args, shell=False, stdin=PIPE,
                stdout=PIPE, stderr=PIPE)
            results = gpg.communicate(message)
        elif filepath:
            pass
        return GnuPGResult(results)

    def decrypt(self, message=None, filepath=None):
        '''Decrypts the message block passed in
        or the file found at filepath

        @rtype GnuPGResult object
        '''
        return self._process_gpg('decrypt', message, filepath)

    def verify(self, message=None, filename=None):
        return self._process_gpg('verify', message, filepath)

    def sign(self, message=None, filename=None, mode=None):
        if not mode:
            return GnuPGResult('', 'pyGPG: Error, no mode signing passed in\n')
        return self._process_gpg(mode, message, filepath)

    def dump_options(self, only_usable=False, refetch=False):
        '''Runs 'gpg --dump-options'
        @param only_usable: Boolean, When True will filter
            the returned list to only contain the options this class
            is capable of using.
        @param refetch: Boolean
        @rtype list: of options from gpg'''
        if not self._gpg_options or refetch:
            self._gpg_options = self._process_gpg('dump-options')
        return self._gpg_options.output.split("\n")

    def version(self, refetch=False):
        '''Runs 'gpg --version'
        @param refetch: Boolean
        @rtype list: of options from gpg'''
        if not self._gpg_version or refetch:
            self._gpg_version = self._process_gpg('version')
        return self._gpg_version.output.split("\n")

    def custom_run(self, **kwargs):
        '''Runs gpg with any options, modes available
        @param **kwargs: dictionary of keyword arguments
        @rtype '''
        pass
