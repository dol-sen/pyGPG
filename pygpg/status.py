#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# pyGPG Status
#################################################################################
# File:       status.py
#
#             Python class for interpreting the results
#             of a gpg operation status messages
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's gpg status output.'''


from pygpg.legend import LEGEND, IDENTIFIER

class Status(object):
    '''Decodes all status messages and
    puts the relavent info into a dictionary'''


    def __init__(self):
        self.messages = []
        self.status_msgs = []
        self.data = {'msgs':set()}
        self.errors = []


    def extract_data(self, messages):
        stderr_msgs = []
        self.messages = messages
        for msg in messages:
            if msg.startswith(IDENTIFIER):
                self.status_msgs.append(msg)
                #print 'msg',msg
                # split it into parts, discard the IDENTIFIER
                parts = msg.split()[1:]
                #print 'parts', parts
                key = parts.pop(0)
                try:
                    status = LEGEND[key]
                except KeyError:
                    continue
                for v in status['data']:
                    if v.startswith('['):
                        # strip the optional data indicator
                        v = v[1:-1]
                        optional = True
                    else:
                        optional = False
                    # now add the key to the variable name to keep them
                    # from overwriting others of the same name,
                    # but possibly different info
                    var_name = '-'.join([key.lower(), v])
                    if parts:
                        self.data[var_name] = parts.pop(0)
                    elif not optional:
                        error = "Missing status data: %s" % var_name
                        self.errors.append("ERROR in data: %s\n<<%s>>\n'"
                            % (error, msg))
                    if status['msg']:
                        self.data['msgs'].add('%s, %s' % (key,status['msg']))
            else:
                stderr_msgs.append(msg)
        return stderr_msgs




