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



import os
import copy
import sys
from subprocess import Popen, PIPE

from pyGPG import __version__, __license__
from pyGPG.output import GPGResult
from pyGPG.legend import PYGPG_IDENTIFIER

if sys.hexversion >= 0x30200f0:
    STR = str
else:
    STR = basestring


class GPG(object):
    '''Subprocess gnupg handler class'''

    def __init__(self, config, logger=None):
        '''Class init function

        @param config: GPGConfig config instance to use
        '''
        self.config = config
        self.logger = logger
        self._gpg_version = None
        self._gpg_options = None
        self.history = []
        self.env = copy.copy(os.environ)


    def runGPG(self, task=None, inputtxt=None, inputfile=None, outputfile=None):
        '''Creates, opens and runs the gpg subprocess,
        you must pass in at least one of either inputtxt or inputfile

        @param task: string, one of pygpg's config['tasks'].keys()
        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @param inputfile: string (optional) a filepath to pass to gpg
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        results = ('', '') # null
        gpg = None
        if not task:
            return None
        args = [self.config.get_key('gpg_command')]
        defaults = self.config.get_key('gpg_defaults')
        if self.logger:
            self.logger.debug("defaults =" + str(defaults))
        args.extend(defaults)
        task_opts = self.config.get_key('tasks', task)
        if task_opts:
            args.extend(task_opts)
        if outputfile:
            args.extend(['-o', outputfile])
        args = [x for x in args if x != '']
        if inputfile and isinstance(inputfile, STR):
            inputfile = [inputfile]
        if inputtxt is None and inputfile is not None:
                inputtxt = ''  # open('/dev/null', 'wb')
                args.append(self.config[task])
                args += inputfile
        elif inputtxt and inputfile is not None:
                args += [self.config[task]] + inputfile + ['-']
        elif inputtxt is None:
            err = GPGResult(None, ['', ''])
            parts = [
                PYGPG_IDENTIFIER,
                'PYGPG_ERROR',
                'no-input-specified',
                'GPG.runGPG()',
                'You must pass in a non-None inputtxt or inputfile to process',
                ]
            err.status.process_pygpg_msg(parts=parts)
            return err
        else:
            args.append(self.config[task])
        # history is only for initial debugging
        #self.history.append(
        if self.logger:
            self.logger.debug("Running gpg with: '%s'" % str(args))
        gpg = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=self.env)
        results = gpg.communicate(inputtxt)
        for pipe in (gpg.stdin, gpg.stdout, gpg.stderr):
            if pipe:
                pipe.close()
        #inputtxt.close()
        if task in ['list-key', 'list-keys', 'fingerprint', 'refresh-keys'] \
                and '--with-colons' in self.config.get_key('tasks', task):
            return GPGResult(gpg, results, extract_stdout=True)
        return GPGResult(gpg, results)

<<<<<<< HEAD
=======
    def runGPG2(self, task=None, inputtxt=None, *args):
        '''Creates, opens and runs the gpg subprocess,
        you must pass in at least one of either inputtxt or inputfile

        @param task: string, one of pygpg's config['tasks'].keys()
        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @param inputfile: string (optional) a filepath to pass to gpg
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        results = ('', '') # null
        gpg = None
        if not task:
            return None
        args2 = [self.config.get_key('gpg_command')]
        defaults = self.config.get_key('gpg_defaults')
        if self.logger:
            self.logger.debug("defaults =" + str(defaults))
        args2.extend(defaults)
        args2.extend(args)

        args2 = [x for x in args2 if x != '']

        args2.append(self.config[task])

        # history is only for initial debugging
        #self.history.append(
        if self.logger:
            self.logger.debug("Running gpg with: '%s'" % str(args2))
        gpg = Popen(args2, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=self.env)

        if self.logger:
            self.logger.debug("inputtxt '%s'" % str(inputtxt))

        results = gpg.communicate(inputtxt)
        for pipe in (gpg.stdin, gpg.stdout, gpg.stderr):
            if pipe:
                pipe.close()
        if self.logger:
            self.logger.debug("results '%s'" % str(results))

        return GPGResult(gpg, results)

>>>>>>> e65b4e2... my version
    def listkey(self, id_string=None, outputfile=None):
        '''Lists the keys with --list-key <argument>

        @param id_string: string (optional) argument to --list-key
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        return self.runGPG('list-key', inputfile=id_string,
                           outputfile=outputfile)

<<<<<<< HEAD
=======
    def importkey(self, inputfile=None):
        '''Import keys with --import <inputfile>

        @param inputfile: string filepath to pass to
                           gpg for the key to import
        @rtype GnuPGResult object
        '''
        return self.runGPG('import', inputfile=inputfile,
                           #outputfile=outputfile
        )

>>>>>>> e65b4e2... my version
    def listkeys(self, id_string=None, outputfile=None):
        '''Lists the keys with --list-keys <argument>

        @param id_string: string (optional) argument to --list-keys
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        return self.runGPG('list-keys', inputfile=id_string,
                           outputfile=outputfile)

    def fingerprint(self, id_string=None, outputfile=None):
        '''Lists the key, with the fingerprint

        @param task: string, one of pygpg's config['tasks'].keys()
        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @param inputfile: string (optional) a filepath to pass to gpg
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        return self.runGPG('fingerprint', inputfile=id_string,
                           outputfile=outputfile)

    def decrypt(self, inputtxt=None, inputfile=None, outputfile=None):
        '''Decrypts the inputtxt block passed in
        or the file found at inputfile and saves it to outputfile,
        and/or returns the decrypted as GPGResult.output

        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @param inputfile: string (optional) a filepath to pass to gpg
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        return self.runGPG('decrypt', inputtxt, inputfile, outputfile)

<<<<<<< HEAD
=======
    def encrypt(self, inputtxt, recipient):
        '''encrypts the inputtxt block passed in
        and/or returns the decrypted as GPGResult.output

        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @rtype GnuPGResult object
        '''
        return self.runGPG2('encrypt', inputtxt, '--recipient',recipient, '--trust-mode', 'always', '--armor')

>>>>>>> e65b4e2... my version

    def verify(self, inputtxt=None, inputfile=None, outputfile=None):
        '''
        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @param inputfile: string (optional) a filepath to pass to gpg
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
        return self.runGPG('verify', inputtxt, inputfile, outputfile)


    def sign(self, mode, inputtxt=None, inputfile=None, outputfile=None):
        '''
        @param inputtxt: string (optional)  of text to send to gpg's stdin
        @param inputfile: string (optional) a filepath to pass to gpg
        @param outputfile: string (optional) filepath to pass to
                           gpg for it's output
        @rtype GnuPGResult object
        '''
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

        checks config parameter refetch: Boolean
        @rtype list: of options from gpg'''
        if not self._gpg_options or self.config['refetch']:
            self._gpg_options = self.runGPG('dump-options', '')
        opts = self._gpg_options.output.split("\n")
        if self.config['only_usable']:
            return list(set(opts.difference(self.config.unsupported)))
        return opts


    def version(self, verbose=False):
        '''Runs 'gpg --version' and also returns the pyGPG version

        checks config parameter refetch: Boolean
        @param verbose: boolean, defaults to False
        @rtype dict: of versions'''
        if (self._gpg_version is None) or self.config['refetch']:
            self._gpg_version = self.runGPG('version', '')
            self._gpg_version.status.process_gpg_ver(self._gpg_version.output.split('\n'))
            # now do pygpg version
            # insert it as the first entry in status.data
            target = []
            parts = [PYGPG_IDENTIFIER, 'PYGPG_VERSION', __version__, __license__]
            self._gpg_version.status.process_pygpg_msg(parts=parts, target=target)
            self._gpg_version.status.data.insert(0, target[0])
        data = self._gpg_version.status.data
        if verbose:
            result = {}
            for x in data:
                result[x.name] = x._asdict()
        return {'pygpg': data[0].pygpg,
                'gpg': data[1].gpg,
                'libcrypt': data[1].libcrypt,
                }
