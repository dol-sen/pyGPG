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

    def _process_gpg(self, args):
        '''Creates and opens the subprocess object
        @rtype Popen object
        '''
        return process = Popen(args, shell=False, stdin=PIPE,
                stdout=PIPE, stderr=PIPE)

    def decrypt(self, message=None, filepath=None):
        '''Decrypts the message block passed in
        or the file found at filepath'''
        results = ('', '') # null
        if message:
            args = [self.config['gpg_command'],
                    self.config['decrypt'],
                    self.config.get_options()
                ]
            gpg = self._process_gpg(args)
            results = gpg.communicate(message)

        elif filepath:
            pass
        return GnuPGResult(results)

    def verify(self, message=None, filename=None):
        pass

    def sign(self, message=None, filename=None, mode=''):
        pass

    def dump_options(self, only_usable=False):
        '''Runs 'gpg --dump-options'
        @param only_usable: Boolean, When True will filter
            the returned list to only contain the options this class
            is capable of using.
        @rtype list: of options from gpg'''

