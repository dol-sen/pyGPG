# File:       test/pyGPG/test_config.py
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
pyGPG/config.py tests

'''

from collections import OrderedDict

from pyGPG.config import GPGConfig

CFG = GPGConfig()


def test_get_key():
    value = CFG.get_key('clearsign')
    print('value:', value)
    assert value == CFG.defaults['clearsign']


def test_sub_list1():
    CFG.options['foo'] = 'LIST-FOO'
    CFG.options['list-foo'] = ['foo', '%(foo)s', 'bar']
    print('value:', CFG.get_key('list-foo')[1])
    assert CFG.get_key('list-foo')[1] == CFG.options['foo']


def test_sub_list2():
    CFG.defaults['bar'] = 'LIST-BAR'
    CFG.options['list-foo'] = ['foo', '%(bar)s', 'bar']
    print('value:', CFG.get_key('list-foo')[1])
    assert CFG.get_key('list-foo')[1] == CFG.defaults['bar']


def test_sub_str1():
    CFG.options['foo'] = 'LIST-FOO'
    CFG.options['str-foo'] = 'foo %(foo)s bar'
    print('value:', CFG.get_key('str-foo'))
    assert CFG.get_key('str-foo') == 'foo LIST-FOO bar'


def test_sub_str2():
    CFG.defaults['bar'] = 'LIST-BAR'
    CFG.options['str-foo'] = 'foo %(bar)s bar'
    print('value:', CFG.get_key('str-foo'))
    assert CFG.get_key('str-foo') == 'foo LIST-BAR bar'


def test_sub_tuple1():
    CFG.options['foo'] = 'LIST-FOO'
    CFG.options['tuple-foo'] = ('foo', '%(foo)s', 'bar')
    print('value:', CFG.get_key('tuple-foo')[1])
    assert CFG.get_key('tuple-foo')[1] == CFG.options['foo']


def test_sub_tuple2():
    CFG.defaults['bar'] = 'LIST-BAR'
    CFG.options['tuple-foo'] = ('foo', '%(bar)s', 'bar')
    print('value:', CFG.get_key('tuple-foo')[1])
    assert CFG.get_key('tuple-foo')[1] == CFG.defaults['bar']


def test_sign_modes1():
    print('value:', CFG.sign_modes())
    assert sorted(CFG.sign_modes()) == sorted(["clearsign", "sign", "detach-sign"])


def test_sign_modes2():
    gpg_modes = set(['sign', 'detach-sign', 'sneaky-sign'])
    print('value:', CFG.sign_modes(gpg_modes))
    assert sorted(CFG.sign_modes(gpg_modes)) == sorted([ "sign", "detach-sign"])


def test_get_defaults():
    assert CFG.get_defaults() == CFG.defaults


def test_getitem():
    assert CFG.__getitem__('foo') == CFG.options['foo']


def test_subkey1():
    CFG.defaults['subkey1'] = {'key1': 'SUBKEY-FOO', 'key2': 'somevalue'}
    print('value:', CFG.get_key('subkey1', 'key1'))
    assert CFG.get_key('subkey1', 'key1') == 'SUBKEY-FOO'


def test_subkey2():
    CFG.options['subkey1'] = {'key2': 'somevalue'}
    print('value:', CFG.get_key('subkey1', 'key1'))
    assert CFG.get_key('subkey1', 'key1') == 'SUBKEY-FOO'


def test_subkey3():
    CFG.options['subkey1'] = {'key2': 'somevalue'}
    print('value:', CFG.get_key('subkey1', 'key1'))
    assert CFG.get_key('subkey1', 'key3') == None


def test_subkey4():
    CFG.options['subkey1'] = {'key2': 'somevalue'}
    print('value:', CFG.get_key('subkey3', 'key1'))
    assert CFG.get_key('subkey3', 'key3') == None


def test_subkey5():
    del CFG.options['subkey1']
    print('value:', CFG.get_key('subkey1', 'key4'))
    assert CFG.get_key('subkey1', 'key4') == None


def test_subkey6():
    CFG.options['foo'] = {'key1': 'DICT-FOO', 'key2': 'FOO-BAR'}
    CFG.options['dict-foo'] = {'foo': '%(foo)s', 'bar': 'dict-bar' }
    print('value:', CFG.get_key('dict-foo', 'foo'))
    assert CFG.get_key('dict-foo', 'foo') == str(CFG.options['foo'])


def test_sub_dict1():
    CFG.defaults['bar'] = {'key1': 'DICT-FOO', 'key2': 'FOO-BAR'}
    CFG.options['dict-foo'] = {'foo': CFG.defaults['bar'], 'bar': 'dict-bar' }
    print('value:', CFG.get_key('dict-foo', 'foo'))
    assert CFG.get_key('dict-foo', 'foo') == CFG.defaults['bar']


def test_sub_nottype():
    CFG.defaults['bar'] = OrderedDict([('key1', 'DICT-FOO'), ('key2', 'FOO-BAR')])
    CFG.options['dict-foo'] = {'foo': CFG.defaults['bar'], 'bar': 'dict-bar' }
    print('value:', CFG.get_key('dict-foo', 'foo'))
    assert CFG.get_key('dict-foo', 'foo') == CFG.defaults['bar']




