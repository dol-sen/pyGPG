#!/usr/bin/python
# -*- coding: utf-8 -*-
####################
# pyGPG GPg mapping constants
####################
# File:       mappings.py
#
#             Python Interface access to gnupg
#
# Copyright:
#             (c) 2014 Brian Dolbec
#             Distributed under the terms of the BSD license
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#



ALGORITHM_CODES = {
    '1': 'RSA',
    '2': 'RSA',      # (encrypt only)
    '3': 'RSA',      # (sign only)
    '16': 'ElGamal', # (encrypt only)
    '17': 'DSA',     #(sometimes called DH, sign only)
    '18': 'ECDH',
    '19': 'ECDSA',
    '20': 'ElGamal', # (sign and encrypt)
    '21': 'Diffie-Hellman',
    '22': 'EdDSA',   # (new) [I-D.irtf-cfrg-eddsa] [RFC6090]
}

CAPABILITY_MAP = {
    'a': 'authenticate',
    'c': 'certify',
    'e': 'encrypt',
    's': 'sign',
    'A': '(Authenticate)',
    'C': '(Certify)',
    'E': '(Encrypt)',
    'S': '(Sign)',
    '?': 'Unknown',
}

VALIDITY_MAP = {
    'o': 'Unknown',
    'i': 'Invalid',
    'd': 'Disabled',
    'r': 'Revoked',
    'e': 'Expired',
    '-': 'Unknown',
    'q': 'Undefined',
    'n': 'Valid',
    'm': 'Marginal',
    'f': 'Fully valid',
    'u': 'Ultimately valid',
}

INVALID_LIST = ['i', 'd', 'r', 'e']
VALID_LIST = ['o', '-', 'q', 'n', 'm', 'f', 'u']

KEY_VERSION_FPR_LEN = {
    32: '3',
    40: '4',
    '3': 32,
    '4': 40,
}
