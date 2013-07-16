#!/usr/bin/env python

import sys

from distutils.core import setup

# this affects the names of all the directories we do stuff with
sys.path.insert(0, './')

from pygpg.version import Version, License


#__version__ = os.getenv('VERSION', default='9999')


setup(name          = 'pyGPG',
      version       = Version,
      description   = "A python interface wrapper for gnupg's gpg command",
      author        = 'Brian Dolbec',
      author_email  = 'dolsen@gentoo.org',
      url           = "https://github.com/dol-sen/pyGPG",
      packages      = ['pyGPG'],
      license       = License,
      )

