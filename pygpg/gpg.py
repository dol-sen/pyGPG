#!/usr/bin/python
# -*- coding: utf-8 -*-
####################
# pyGPG GPG handler
####################
# File:       gnupg.py
#
#             Python Interface access to gnupg
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the BSD license
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
from pygpg.version import Version, License
from pygpg.legend import PYGPG_IDENTIFIER


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


    def runGPG(self, action=None, inputtxt=None, inputfile=None, outputfile=None):
        '''Creates, opens and runs the gpg subprocess
        @rtype GnuPGResult object
        '''
        results = ('', '') # null
        gpg = None
        if not action:
            return None
        args = [self.config['gpg_command']]
        args.extend(self.config['gpg_defaults'])
        task_opts = self.config.get_key('tasks', action)
        if task_opts:
            args.extend(task_opts)
        if outputfile:
            args.extend(['-o',outputfile])
        args = [x for x in args if x != '']
        if inputtxt is None and inputfile is not None:
                inputtxt = open('/dev/null', 'wb')
                args.extend([self.config[action], inputfile])
        if inputtxt and inputfile is not None:
                args.extend([self.config[action], inputfile, '-'])
        elif inputtxt is None:
            err = GPGResult(None, ['',''])
            parts = [PYGPG_IDENTIFIER, 'PYGPG_ERROR',
                'no-input-specified', 'GPG.runGPG()',
                'You must pass in a non-None inputtxt or inputfile to process']
            err.status.process_pygpg_msg(parts=parts)
            return err
        else:
            args.append(self.config[action])
        # history is only for initial debugging
        #self.history.append(
        print "Running gpg with: '%s'" % str(args)
        gpg = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=self.env)
        results = gpg.communicate(inputtxt)
        #inputtxt.close()
        return GPGResult(gpg, results)


    def decrypt(self, inputtxt=None, inputfile=None, outputfile=None):
        '''Decrypts the inputtxt block passed in
        or the file found at inputfile and saves it to outputfile,
        and/or returns the decrypted as GPGResult.output

        @rtype GnuPGResult object
        '''
        return self.runGPG('decrypt', inputtxt, inputfile, outputfile)


    def verify(self, inputtxt=None, inputfile=None, outputfile=None):
        return self.runGPG('verify', inputtxt, inputfile, outputfile)


    def sign(self, mode, inputtxt=None, inputfile=None, outputfile=None):
        if mode not in self.config.sign_modes():
            return GPGResult(None, '', 'pyGPG: Error, no/unsupported signing'
                'mode passed in: %s\n' % mode)
        return self.runGPG(mode, inputtxt, inputfile, outputfile)


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


    def version(self, verbose=False):
        '''Runs 'gpg --version'
        @param refetch: Boolean
        @rtype dict: of versions'''
        if (self._gpg_version is None) or self.config['refetch']:
            self._gpg_version = self.runGPG('version', '')
            self._gpg_version.status.process_gpg_ver(self._gpg_version.output.split('\n'))
            # now do pygpg version
            # insert it as the first entry in status.data
            target = []
            parts = [PYGPG_IDENTIFIER, 'PYGPG_VERSION', Version, License]
            self._gpg_version.status.process_pygpg_msg(parts=parts, target=target)
            self._gpg_version.status.data.insert(0,target[0])
        data = self._gpg_version.status.data
        if verbose:
            result = {}
            for x in data:
                result[x.name] = x._asdict()
        return {'pygpg':data[0].pygpg, 'gpg':data[1].gpg,
            'libcrypt':data[1].libcrypt}

