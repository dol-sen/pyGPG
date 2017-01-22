#!python
# -*- coding: utf-8 -*-

import os

from pyGPG import __version__
from pyGPG.config import GPGConfig
from pyGPG.gpg import GPG



def test_gpg_version1():
    import logging
    logger = logging.getLogger('pyGPG-testing')
    logger.setLevel(logging.DEBUG)
    cfg = GPGConfig()
    cfg.options['gpg_command'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpg-version')
    gpg = GPG(cfg, logger=logger)
    v = gpg.version()
    print("****", cfg.get_key('gpg_command'))
    print("****", v)
    assert v == {'gpg': '2.1.75', 'pygpg': __version__, 'libcrypt': '1.7.5'}


def test_gpg_version2():
    from collections import OrderedDict
    cfg = GPGConfig()
    cfg.options['gpg_command'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpg-version')
    gpg = GPG(cfg)
    v = gpg.version(verbose=True)
    print("****", cfg.get_key('gpg_command'))
    print("****", v)
    assert v == {
        'GPG_VERSION': OrderedDict([
            ('gpg', '2.1.75'),
            ('libcrypt', '1.7.5'),
            ('copyright', '(C) 2016 Free Software Foundation, Inc.'),
            ('license', 'GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>'),
            ('home', '/home/brian/.gnupg'),
            ('sup_pubkey', 'RSA, ELG, DSA, ECDH, ECDSA, EDDSA'),
            ('sup_cipher', 'IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH, CAMELLIA128, CAMELLIA192, CAMELLIA256'),
            ('sup_hash', 'SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224'),
            ('sup_compress', 'Uncompressed, ZIP, ZLIB, BZIP2')]),
        'PYGPG_VERSION': OrderedDict([('pygpg', '0.2'), ('license', 'BSD')])
        }


def test_gpg_options1():
    cfg = GPGConfig()
    cfg.options['gpg_command'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpg-options')
    gpg = GPG(cfg)
    v = sorted(gpg.options)
    print("****", cfg.get_key('gpg_command'))
    print("****", len(v), v[0], v[23], v[-1])
    assert len(v) == 381
    assert v[0] == '--agent-program'
    assert v[23] == '--cert-digest-algo'
    assert v[-1] == '--yes'

def test_gpg_options2():
    cfg = GPGConfig()
    cfg.options['gpg_command'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpg-options')
    cfg.options['only_usable'] = True
    cfg.unsupported = set(['--agent-program', '--passphrase-fd', '--cert-digest-algo', '--passphrase-repeat',
                           '--yes'])
    gpg = GPG(cfg)
    v = sorted(gpg.options)
    print("****", cfg.get_key('gpg_command'))
    print("****", len(v), v[0], v[23], v[-1])
    assert len(v) == 376
    assert v[0] == '--allow-freeform-uid'
    assert v[23] == '--cert-policy-url'
    assert v[-1] == '--xauthority'


