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


# import legend for getattr(legend, '{class}') use
# that way we only retrieve the class(es) we actually need
from pygpg import legend

from pygpg.legend import (
    GPG_IDENTIFIER,
    PYGPG_IDENTIFIER,
    GPG_VER_IDENTFIER
)


class Status(object):
    '''Decodes all status messages and
    puts the relavent info into lists'''


    def __init__(self):
        self.messages = []
        self.status_msgs = []
        self.data = []
        self.errors = []


    def extract_data(self, messages):
        stderr_msgs = []
        self.messages = messages
        for msg in messages:
            if self.isinstance_msg(GPG_IDENTIFIER, msg):
                self.process_status_msg(msg)
            # pyGPG version info is first in the list
            elif self.isinstance_msg(PYGPG_IDENTIFIER, msg):
                self.process_pygpg_msg(msg)
            elif self.isinstance_msg(GPG_VER_IDENTFIER, msg):
                self.process_gpg_ver(messages[1:])
                break
            else:
                stderr_msgs.append(msg)
        return stderr_msgs


    @staticmethod
    def isinstance_msg(identifier, msg):
        return identifier in msg


    @staticmethod
    def _split_message(msg):
        # split it into [*_IDENTIFIER, key, data] parts
        # discard the *_IDENTIFIER
        # we are not yet spliting the actual data
        alerts = []
        parts = msg.split(' ', 2)[1:]
        key = parts.pop(0)
        try:
            status = getattr(legend, key)
        except AttributeError:
            alerts.append((self.errors, [PYGPG_IDENTIFIER, 'PYGPG_ATTRIBUTE_ERROR',
                legend, key]))
            return (None, parts, alerts)
        # need to handle <username> fields that would split
        # into many parts instead of just the one
        num_fields = len(status._fields)
        if num_fields != len(parts):
            #print 'field parts', parts
            if parts is not [] and len(parts) == 1:
                parts = parts[0].split(' ', num_fields -1)
            missing = num_fields - len(parts)
            #print num_fields,missing, 'parts', parts
            while missing > 0:
                parts.append(None)
                missing -= 1
            if missing < 0:  # uh-oh too much info
                alerts.append((self.errors, [PYGPG_IDENTIFIER, 'PYGPG_UNEXPECTED_DATA',
                    key, str(status._fields), str(parts[missing:])]))
                # it's being logged, so trim off the extra
                # to prevent a traceback
                parts = parts[:missing]
        return (status, parts, alerts)


    def process_status_msg(self, msg):
        self.status_msgs.append(msg)
        status, parts, alerts = self._split_message(msg)
        if status:
            self.data.append(status._make(parts))
        for target, alert in alerts:
            self.process_pygpg_msg(parts=alert, target=target)
        return


    def process_pygpg_msg(self, message=None, parts=None, target=None):
        if target is None:
            target = self.data
        if message is not None:
            status = getattr(legend, 'PYGPG_MESSAGE')
            target.append(status._make([message]))
        elif parts is not None:
            status = getattr(legend, parts[1])
            target.append(status._make(parts[2:]))


    def process_gpg_ver(self, messages):
        msg_keys = ['gpg', 'libgcrypt', 'Copyright',
            'License', 'Home:', 'Pubkey:', 'Cipher:', 'Hash:', 'Compression:']
        parts = {}
        multiline = False
        for msg in messages :
            #print msg
            if not msg:
                #print '====>', 'skipping'
                continue
            if multiline:
                #print '====>', 'multiline'
                parts[key] += ' ' + msg.strip()
                if not parts[key].endswith(','):
                    #print '    ====>', 'multiline OFF'
                    multiline = False
            else:
                key = msg.split()[0]
                if key in msg_keys:
                    if key in ['gpg', 'libgcrypt']:
                        parts[key] = msg.rsplit(' ', 1)[1]
                    else:
                        parts[key] = msg.split(' ', 1)[1].strip()
                        #print '====>', 'key;', key, 'data:', parts[key][-10:]
                        if parts[key].endswith(','):
                            #print '====>', 'new multiline'
                            multiline = True
        # store the data in the correct order
        field_data = []
        for k in msg_keys:
            field_data.append(parts[k])
        status = getattr(legend, 'GPG_VERSION')
        self.data.append(status._make(field_data))




