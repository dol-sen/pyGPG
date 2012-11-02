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


from pygpg import legend
from pygpg.legend import IDENTIFIER


class Status(object):
    '''Decodes all status messages and
    puts the relavent info into a dictionary'''


    def __init__(self):
        self.messages = []
        self.status_msgs = []
        self.data = []
        self.errors = []


    def extract_data(self, messages):
        stderr_msgs = []
        self.messages = messages
        for msg in messages:
            if self._is_status_msg(msg):
                self.status_msgs.append(msg)
                # split it into [IDENTIFIER, key, data] parts
                # discard the IDENTIFIER
                # we are not yet spliting the actual data
                parts = msg.split(' ', 2)[1:]
                key = parts.pop(0)
                try:
                    status = getattr(legend, key)
                except AttributeError:
                    self.errors.append("ERROR getting status class %s" % key)
                    continue
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
                        self.errors.append(
                            "Found unexpected data for %s, fields=%s, data=%s"
                            %( key, str(status._fields), str(parts)))
                        self.errors.append(key + ' ' + str(parts[missing:]))
                        # it's been logged, so trim off the extra
                        # to prevent a traceback
                        parts = parts[:missing]
                self.data.append(status._make(parts))
            else:
                stderr_msgs.append(msg)
        return stderr_msgs

    @staticmethod
    def _is_status_msg(msg):
        return IDENTIFIER in msg


