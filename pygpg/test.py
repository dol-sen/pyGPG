#!python
# -*- coding: utf-8 -*-



# live testing cmds.
#


from pygpg.config import GPGConfig
from pygpg.gpg import GPG;c=GPGConfig()

gpg=GPG(c);v=gpg.version

def ds():

    asc=open('/home/brian/layman-test/repositories.xml.asc', 'r').read()

    d=gpg.decrypt(gpg_input=asc)

    pl=open('/home/brian/layman-test/installed.xml', 'r').read()

    s=gpg.sign('clearsign', gpg_input=pl)

    return d,s

