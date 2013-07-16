#!python
# -*- coding: utf-8 -*-



# live testing cmds.
#


from pyGPG.config import GPGConfig
from pyGPG.gpg import GPG

c=GPGConfig()

gpg=GPG(c)

v=gpg.version()

def ds():

    asc=open('/home/brian/layman-test/repositories.xml.asc', 'r').read()

    d=gpg.decrypt(inputtxt=asc)

    pl=open('/home/brian/layman-test/installed.xml', 'r').read()

    s=gpg.sign('clearsign', inputtxt=pl)

    return d,s

