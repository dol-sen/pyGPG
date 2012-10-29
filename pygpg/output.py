#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# pyGPG GnuPGResult
#################################################################################
# File:       output.py
#
#             Python class for interpreting the results
#             of a gpg operation
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's gpg output.'''



class GPGResult(object):
    '''GnuPG process result handler'''

    def __init__(self, gpg, results):
        self.gpg = gpg
        self.output = results[0]
        self.messages = results[1].split('\n')
        self._time = None
        self._signature = None
        self._key_id = None
        self._key_type = None
        self._fingerprint = None

    @property
    def verified(self):
        pass

    @property
    def time(self):
        pass

    @property
    def key_id(self):
        pass

    @property
    def key_type(self):
        pass

    @property
    def signature(self):
        pass

    @property
    def returncode(self):
        return self.gpg.returncode
