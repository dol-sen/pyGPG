# File:       test/pyGPG/test_legend.py
#
#             Python Interface access to gnupg
#
# Copyright:
#             (c) 2017 Brian Dolbec
#             Distributed under the terms of the BSD license
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#

'''
pyGPG/legend.py tests

'''

# There is not much to test here, so a
# simple import of everything and
# testing that one class is useable should suffice

from pyGPG.legend import *


def test_classes():
    klass = PYGPG_VERSION('0.1.0', 'BSD')
    assert isinstance(klass, PYGPG_VERSION)
