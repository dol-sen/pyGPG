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
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Handles pyGPG's gpg status output.'''

import sys

if sys.version_info[0] >= 3:
    def decoder(text, enc='utf_8'):
        return text

    # pylint: disable=W0622
    basestring = str
else:
    def decoder(text, enc='utf_8'):
        return unicode(text)


# import legend for getattr(legend, '{class}') use
# that way we only retrieve the class(es) we actually need
from pyGPG import legend

from pyGPG.legend import (
    GPG_IDENTIFIER,
    PYGPG_IDENTIFIER,
    GPG_VER_IDENTFIER,
    COLON_IDENTIFIERS
)


class Status(object):
    '''Parses all status messages and
    puts the relavent info into the various lists'''


    def __init__(self):
        '''Class init function'''
        self.messages = []
        self.status_msgs = []
        self.data = []
        self.errors = []


    def extract_data(self, messages):
        '''Identifies the different message types and
        calls the specifc processing function.

        @param messages: list of string messages to parse
        @rtype list: of stderr messages found
        '''
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
        '''Class specific message type comparision function

        @param identifier: string
        @param msg: string
        @rtype bool
        '''
        return identifier in msg


    def _split_message(self, msg):
        '''Internal message splitting function

        @param msg string
        @rtype tuple: (status, parts, alerts)
        '''
        # split it into [*_IDENTIFIER, key, data] parts
        # discard the *_IDENTIFIER
        # we are not yet spliting the actual data
        alerts = []
        parts = msg.split(' ', 2)[1:]
        key = parts.pop(0)
        try:
            status = getattr(legend, key)
        except AttributeError:
            alerts.append(
                (self.errors, [PYGPG_IDENTIFIER, 'PYGPG_ATTRIBUTE_ERROR',
                               legend, key]))
            return (None, parts, alerts)
        # need to handle <username> fields that would split
        # into many parts instead of just the one
        num_fields = len(status._fields)
        if num_fields != len(parts):
            #print 'field parts', parts
            if parts is not [] and len(parts) == 1:
                parts = parts[0].split(' ', num_fields - 1)
            missing = num_fields - len(parts)
            #print num_fields,missing, 'parts', parts
            while missing > 0:
                parts.append(None)
                missing -= 1
            if missing < 0:  # uh-oh too much info
                alerts.append(
                    (self.errors, [PYGPG_IDENTIFIER, 'PYGPG_UNEXPECTED_DATA',
                                   key, str(status._fields), str(parts[missing:])]))
                # it's being logged, so trim off the extra
                # to prevent a traceback
                parts = parts[:missing]
        return (status, parts, alerts)


    def process_status_msg(self, msg):
        '''Generic message processing function

        @param msg: string
        @modified self.data may be appended with additional data
        @rtype None
        '''
        self.status_msgs.append(msg)
        status, parts, alerts = self._split_message(msg)
        if status:
            self.data.append(status._make(parts))
        for target, alert in alerts:
            self.process_pygpg_msg(parts=alert, target=target)
        return


    def process_pygpg_msg(self, message=None, parts=None, target=None):
        '''Pygpg message processing function

        @param msg: string (optional)
        @param parts: list of strings
        @param target: class variable to modify
        @rtype None
        '''
        if target is None:
            target = self.data
        if message is not None:
            status = getattr(legend, 'PYGPG_MESSAGE')
            target.append(status._make([message]))
        elif parts is not None:
            status = getattr(legend, parts[1])
            target.append(status._make(parts[2:]))


    def process_gpg_ver(self, messages):
        '''GPG message processing function

        @param messages: list of strings
        @modified self.data may be appended with additional data
        @rtype None
        '''
        msg_keys = ['gpg', 'libgcrypt', 'Copyright',
                    'License', 'Home:', 'Pubkey:', 'Cipher:', 'Hash:', 'Compression:']
        parts = {}
        multiline = False
        for msg in messages:
            #print msg
            if not msg:
                #print('====>', 'skipping')
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
            try:
                field_data.append(parts[k])
            except KeyError:
                #print("k", k, "parts", parts)
                pass
        if field_data:
            status = getattr(legend, 'GPG_VERSION')
            self.data.append(status._make(field_data))


    def extract_output(self, messages):
        '''Identifies the different message types and
        calls the specifc processing function.

        @param messages: list of string messages to parse
        @rtype list: of unknown messages found
        '''
        msgs = []
        self.messages = messages
        #print "STATUS: processing messagess:", messages
        for msg in decoder(messages).split('\n'):
            #print "STATUS: processing msg:", msg
            unknown = self.process_colon_listing(msg)
            if unknown:
                msgs.append(unknown)
        #print "STATUS: data =", self.data
        return msgs


    def process_colon_listing(self, msg):
        '''Generic message processing function

        @param msg: string
        @modified self.data may be appended with additional data
        @rtype None
        '''
        self.status_msgs.append(msg)
        parts = msg.split(':')[:13]
        key = parts.pop(0).upper()
        #print("STATUS: key", key, ", parts:", parts)
        if key in COLON_IDENTIFIERS:
            status = getattr(legend, key)
            if key in ["UID", "UAT"] and len(parts)==10:
                parts.extend(['', ''])
            self.data.append(status._make(parts))
            return None
        return msg

