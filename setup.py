#!/usr/bin/env python

import os
import sys

from distutils.core import Command, setup
from pyGPG import __version__, __license__
# this affects the names of all the directories we do stuff with
sys.path.insert(0, './')

#__version__ = os.getenv('VERSION', default='9999')


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        testpath = 'test'
        covpath = ['--cov=' +  p for p in ['pyGPG']]
        errno = subprocess.call(['py.test', '-v', testpath] + covpath + ['--cov-report=html', '--cov-report=term'])
        raise SystemExit(errno)


setup(
    name='pyGPG',
    version=__version__,
    description="A Python interface wrapper for GnuPG's gpg command",
    author='Brian Dolbec',
    author_email='dolsen@gentoo.org',
    url="https://github.com/dol-sen/pyGPG",
    packages=['pyGPG'],
    license=__license__,
    long_description=open('README').read(),
    keywords='gpg',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Security :: Cryptography',
    ],
    cmdclass={'test': PyTest},
)
