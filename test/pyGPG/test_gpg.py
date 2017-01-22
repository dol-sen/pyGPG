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


def test_runGPG1():
    cfg = GPGConfig()
    gpg = GPG(cfg)
    v = gpg.runGPG()
    assert v == None


def test_listkeys1():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['list-keys'] = ['--homedir', homedir]
    print("****", cfg.get_key('tasks', 'list-keys'))
    gpg = GPG(cfg)
    v = gpg.listkeys()
    assert v.returncode == -1
    assert v.output == ''
    assert v.stderr_out == ['']

def test_listkeys2():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['list-keys'] = ['--homedir', homedir]
    print("****", cfg.get_key('tasks', 'list-keys'))
    gpg = GPG(cfg)
    v = gpg.listkeys('0xABB2F2DC74991EE9')
    print("**** keytype", v.keytype)
    assert v.keyid == []
    assert v.fingerprint == []
    assert v.username == []
    assert v.keytype == []
    assert v.output == '''pub   rsa4096/0xABB2F2DC74991EE9 2017-01-22 [C] [expires: 2020-01-07]
      476935D6D659B4C27B700FEDABB2F2DC74991EE9
uid                   [ultimate] pyGPG Test <pygpg@nowhere.foo>
sub   rsa4096/0xA9661AC8014A7CF0 2017-01-22 [S] [expires: 2020-01-07]

'''
    assert v.stderr_out == ['[GNUPG:] KEY_CONSIDERED 476935D6D659B4C27B700FEDABB2F2DC74991EE9 0', '']


def test_listkey1():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['list-key'] = ['--homedir', homedir]
    print("****", cfg.get_key('tasks', 'list-key'))
    gpg = GPG(cfg)
    v = gpg.listkey()
    assert v.output == ''
    assert v.stderr_out == ['']


def test_listkey2():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['list-key'] = ['--homedir', homedir]
    print("****", cfg.get_key('tasks', 'list-key'))
    gpg = GPG(cfg)
    v = gpg.listkey('0xABB2F2DC74991EE9')
    assert v.keyid == []
    assert v.fingerprint == []
    assert v.username == []
    assert v.keytype == []
    assert v.output == '''pub   rsa4096/0xABB2F2DC74991EE9 2017-01-22 [C] [expires: 2020-01-07]
      476935D6D659B4C27B700FEDABB2F2DC74991EE9
uid                   [ultimate] pyGPG Test <pygpg@nowhere.foo>
sub   rsa4096/0xA9661AC8014A7CF0 2017-01-22 [S] [expires: 2020-01-07]

'''
    assert v.stderr_out == ['[GNUPG:] KEY_CONSIDERED 476935D6D659B4C27B700FEDABB2F2DC74991EE9 0', '']

def test_listkey3():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['list-key'] = ['--homedir', homedir, '--with-colons']
    print("****", cfg.get_key('tasks', 'list-key'))
    gpg = GPG(cfg)
    v = gpg.listkey('0xABB2F2DC74991EE9')
    assert v.stderr_out == ['[GNUPG:] KEY_CONSIDERED 476935D6D659B4C27B700FEDABB2F2DC74991EE9 0', '']
    assert v.keyid == [('PUB', 'long_keyid', 'ABB2F2DC74991EE9'), ('SUB', 'long_keyid', 'A9661AC8014A7CF0')]
    assert v.fingerprint == [('FPR', 'fingerprint', '476935D6D659B4C27B700FEDABB2F2DC74991EE9'),
                             ('FPR', 'fingerprint', '884D0847E08005BC1E6DA041A9661AC8014A7CF0')]
    assert v.username == [('UID', 'user_ID', 'pyGPG Test <pygpg@nowhere.foo>')]
    assert v.keytype == []



def test_fingerprint1():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['fingerprint'] = ['--homedir', homedir]
    print("****", cfg.get_key('tasks', 'fingerprint'))
    gpg = GPG(cfg)
    v = gpg.fingerprint()
    assert v.output == ''
    assert v.stderr_out == ['']

def test_fingerprint2():
    cfg = GPGConfig()
    homedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gpghome')
    print("****", homedir)
    cfg.options['tasks']['fingerprint'] = ['--homedir', homedir, '--with-colons']
    print("****", cfg.get_key('tasks', 'fingerprint'))
    gpg = GPG(cfg)
    v = gpg.fingerprint('0xABB2F2DC74991EE9')
    assert v.keyid == [('PUB', 'long_keyid', 'ABB2F2DC74991EE9'), ('SUB', 'long_keyid', 'A9661AC8014A7CF0')]
    assert v.fingerprint == [('FPR', 'fingerprint', '476935D6D659B4C27B700FEDABB2F2DC74991EE9'),
                             ('FPR', 'fingerprint', '884D0847E08005BC1E6DA041A9661AC8014A7CF0')]
    assert v.username == [('UID', 'user_ID', 'pyGPG Test <pygpg@nowhere.foo>')]
    assert v.output == '''tru::1:1485105495:1578417368:3:1:5
pub:u:4096:1:ABB2F2DC74991EE9:1485105368:1578417368::u:::cSC:::::::
fpr:::::::::476935D6D659B4C27B700FEDABB2F2DC74991EE9:
uid:u::::1485105368::64D29249C3C521D9557A5AE461B02179C7D5F227::pyGPG Test <pygpg@nowhere.foo>:
sub:u:4096:1:A9661AC8014A7CF0:1485105368:1578417368:::::s::::::
fpr:::::::::884D0847E08005BC1E6DA041A9661AC8014A7CF0:
'''
    assert v.stderr_out == ['[GNUPG:] KEY_CONSIDERED 476935D6D659B4C27B700FEDABB2F2DC74991EE9 0', '']
