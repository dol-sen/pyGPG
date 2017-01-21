# File:       test/pyGPG/test_mappings.py
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
pyGPG/mappings.py tests

'''

# There is nothing to test here really
# These are not used in pyGPG, but supplied for
# convienience use by consumer applications.


def test_ALGORITHM_CODES():
    from pyGPG.mappings import ALGORITHM_CODES
    assert isinstance(ALGORITHM_CODES, dict)
    assert len(ALGORITHM_CODES) >= 10


def test_CAPABILITY_MAP():
    from pyGPG.mappings import CAPABILITY_MAP
    assert isinstance(CAPABILITY_MAP, dict)
    assert len(CAPABILITY_MAP) >= 9


def test_VALIDITY_MAP():
    from pyGPG.mappings import VALIDITY_MAP
    assert isinstance(VALIDITY_MAP, dict)
    assert len(VALIDITY_MAP) >= 11


def test_KEY_VERSION_FPR_LEN():
    from pyGPG.mappings import KEY_VERSION_FPR_LEN
    assert isinstance(KEY_VERSION_FPR_LEN, dict)
    assert len(KEY_VERSION_FPR_LEN) == 4


def test_VALID_LIST():
    from pyGPG.mappings import VALID_LIST
    assert isinstance(VALID_LIST, list)
    assert len(VALID_LIST) == 7


def test_INVALID_LIST():
    from pyGPG.mappings import INVALID_LIST
    assert isinstance(INVALID_LIST, list)
    assert len(INVALID_LIST) == 4

