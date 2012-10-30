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

#import pygpg
#from pygpg import output
from pygpg.output import GPGResult

# live testing cmds.
# import pygpg;from pygpg.config import GPGConfig;from pygpg.gpg import GPG;c=GPGConfig();gpg=GPG(c);v=gpg.version;asc=open('/home/brian/layman-test/repositories.xml.asc', 'r').read();d=gpg.decrypt(gpg_input=asc);pl=open('/home/brian/layman-test/installed.xml', 'r').read();s=gpg.sign('clearsign', gpg_input=pl)


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


    def _process_gpg(self, action, gpg_input=None, filepath=None, _shell=True):
        '''Creates and opens the subprocess object
        @rtype GnuPGResult object
        '''
        results = ('', '') # null
        gpg = None
        if gpg_input is not None:
            args = [self.config['gpg_command'],
                    self.config['gpg_defaults']]
            if self.config.task_options[action]:
                args.append(self.config.task_options[action])
            args.append(self.config[action])
            # need to pass a string not a list or
            # the status messages won't be ouput
            cmd = ' '.join(args)
            self.history.append("Running gpg with: '%s'" % cmd)
            gpg = Popen(cmd, shell=_shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            results = gpg.communicate(gpg_input)
        elif filepath is not None:
            pass
        return GPGResult(gpg, results)

    def decrypt(self, gpg_input=None, filepath=None, shell=True):
        '''Decrypts the gpg_input block passed in
        or the file found at filepath

        @rtype GnuPGResult object
        '''
        return self._process_gpg('decrypt', gpg_input, filepath, shell)

    def verify(self, gpg_input=None, filepath=None, shell=True):
        return self._process_gpg('verify', gpg_input, filepath, shell)

    def sign(self, mode, gpg_input=None, filepath=None, shell=True):
        if mode not in self.config.sign_modes():
            return GPGResult(None, '', 'pyGPG: Error, no/unsupported signing'
                'mode passed in: %s\n' % mode)
        return self._process_gpg(mode, gpg_input, filepath, shell)

    @property
    def dump_options(self):
        '''Runs 'gpg --dump-options'
        @param only_usable: Boolean, When True will filter
            the returned list to only contain the options this class
            is capable of using.
        @param refetch: Boolean
        @rtype list: of options from gpg'''
        if not self._gpg_options or self.config['refetch']:
            self._gpg_options = self._process_gpg('dump-options', '')
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
            self._gpg_version = self._process_gpg('version', '')
        return self._gpg_version.output.split("\n")

    def custom_run(self, **kwargs):
        '''Runs gpg with any options, modes available
        @param **kwargs: dictionary of keyword arguments
        @rtype '''
        pass
