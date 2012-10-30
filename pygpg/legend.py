#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# pyGPG LEGEND
#################################################################################
# File:       legend.py
#
#             LEGEND data for interpreting the results
#             of gpg operation status messages
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Holds pyGPG's gpg status output legend.'''


# make this global, so is easy to change, and calculates only once
IDENTIFIER = '[GNUPG:] '
ID_LEN = len(IDENTIFIER)

LEGEND = {
    'NEWSIG': {
        'data':[],
        'msg':"Issued right before a signature verification starts."},
    'GOODSIG': {
        'data':['long-keyid', 'username'],
        'msg':"The signature with the keyid is good."},
    'EXPSIG': {
        'data':['long-keyid', 'username'],
        'msg':"The signature with the keyid is good, but the signature is expired."},
    'EXPKEYSIG': {
        'data':['long-keyid', 'username'],
        'msg':"The signature with the keyid is good, but the signature was made by an expired key."},
    'REVKEYSIG': {
        'data':['long-keyid', 'username'],
        'msg':"The signature with the keyid is good, but the signature was made by a revoked key."},
    'BADSIG': {
        'data':['long-keyid', 'username'],
        'msg':"The signature with the keyid has not been verified okay."},
    'ERRSIG':  {
        'data':['long-keyid', 'pubkey_algo', 'hash_algo'
            'sig_class', 'timestamp', 'rc'],
        'msg':"It was not possible to check the signature."},
    'VALIDSIG': {
        'data':['fingerprint', 'sig_creation_date', 'sig-timestamp',
            'expire-timestamp',  'sig-version', 'reserved', 'pubkey-algo',
            'hash-algo', 'sig-class','[primary-key-fpr]'],
        'msg':"The signature with the keyid is good."},
    'SIG_ID':{
        'data':['radix64_string',  'sig_creation_date',  'sig-timestamp'],
        'msg':"This is emitted only for signatures of class 0 or 1 which have been verified okay."},
    'ENC_TO': {
        'data':['long-keyid',  'keytype',  'keylength'],
        'msg':"The message is encrypted to this LONG_KEYID."},
    'NODATA': {
        'data':['what'],
        'msg':"""No data has been found. Codes for what are:
        1 - No armored data.
        2 - Expected a packet but did not found one.
        3 - Invalid packet found, this may indicate a non OpenPGP
                message.
            4 - signature expected but not found
    You may see more than one of these status lines."""},

    'UNEXPECTED': {
        'data':['what'],
        'msg':"Unexpected data has been encountered, 0 - not further specified"},
    'TRUST_UNDEFINED': {
        'data':['error-token'],
        'msg':[]},
    'TRUST_NEVER': {
        'data':['error-token'],
        'msg':"For good signatures, this indicates the validity of the key used to create the signature."},
    'TRUST_MARGINAL': {
        'data':[ '[0]','[validation_model]'],
        'msg':"For good signatures, this indicates the validity of the key used to create the signature."},
    'TRUST_FULLY': {
        'data':['[0]', '[validation_model]'],
        'msg':"For good signatures, this indicates the validity of the key used to create the signature."},
    'TRUST_ULTIMATE': {
        'data':['[0]','[validation_model]'],
        'msg':"For good signatures, this indicates the validity of the key used to create the signature."},
    'PKA_TRUST_GOOD': {
        'data':['mailbox'],
        'msg':"A status code emitted in addition to a TRUST_* status."},
    'PKA_TRUST_BAD': {
        'data':[ 'mailbox'],
        'msg':"A status code emitted in addition to a TRUST_* status."},
    'SIGEXPIRED': {
        'data':[],
        'msg':"This is deprecated in favor of KEYEXPIRED."},
    'KEYEXPIRED': {
        'data':['expire-timestamp'],
        'msg':"The key has expired.  expire-timestamp is the expiration time in seconds since Epoch."},
    'KEYREVOKED': {
        'data':[],
        'msg':"The used key has been revoked by its owner."},
    'BADARMOR': {
        'data':[],
        'msg':"The ASCII armor is corrupted."},
    'RSA_OR_IDEA': {
        'data':[],
        'msg':"The IDEA algorithms has been used in the data."},
    'SHM_INFO': {
        'data':[],
        'msg':""},
    'SHM_GET': {
        'data':[],
        'msg':""},
    'SHM_GET_BOOL': {
        'data':[],
        'msg':""},
    'SHM_GET_HIDDEN': {
        'data':[],
        'msg':""},
    'GET_BOOL': {
        'data':[],
        'msg':""},
    'GET_LINE': {
        'data':[],
        'msg':""},
    'GET_HIDDEN': {
        'data':[],
        'msg':""},
    'GOT_IT': {
        'data':[],
        'msg':""},
    'NEED_PASSPHRASE': {
        'data':['long-main-keyid', 'long-keyid', 'keytype', 'keylength'],
        'msg':"Issued whenever a passphrase is needed."},
    'NEED_PASSPHRASE_SYM': {
        'data':['cipher_algo', 's2k_mode', 's2k_hash'],
        'msg':"Issued whenever a passphrase for symmetric encryption is needed."},
    'NEED_PASSPHRASE_PIN': {
        'data':['card_type', 'chvno', 'serialno',],
        'msg':"Issued whenever a PIN is requested to unlock a card."},
    'MISSING_PASSPHRASE': {
        'data':[],
        'msg':"No passphrase was supplied."},
    'BAD_PASSPHRASE': {
        'data':['long-keyid'],
        'msg':"The supplied passphrase was wrong or not given."},
    'GOOD_PASSPHRASE': {
        'data':[],
        'msg':"The supplied passphrase was good and the secret key material is therefore usable."},
    'DECRYPTION_FAILED': {
        'data':[],
        'msg':"The symmetric decryption failed - one reason could be a wrong passphrase for a symmetrical encrypted message."},
    'DECRYPTION_OKAY': {
        'data':[],
        'msg':"The decryption process succeeded."},
    'NO_PUBKEY': {
        'data':['long-keyid'],
        'msg':"The key is not available"},
    'NO_SECKEY': {
        'data':[  'long-keyid',],
        'msg':"The key is not available"},
    'IMPORT_CHECK': {
        'data':['long-keyid', 'fingerprint', 'user-ID'],
        'msg':'This status is emitted in interactive mode right before the "import.okay" prompt.'},
    'IMPORTED': {
        'data':['long-keyid', 'username'],
        'msg':"The keyid and name of the signature just imported"},
    'IMPORT_OK': {
        'data':[  'reason', ['fingerprint',]],
        'msg':"""The key with the primary key's FINGERPRINT has been imported.
        Reason flags:
          0 := Not actually changed
          1 := Entirely new key.
          2 := New user IDs
          4 := New signatures
          8 := New subkeys
         16 := Contains private key.
        The flags may be ORed."""},

    'IMPORT_PROBLEM': {
        'data':['reason', '[fingerprint]'],
        'msg':"""Issued for each import failure.  Reason codes are:
          0 := "No specific reason given".
          1 := "Invalid Certificate".
          2 := "Issuer Certificate missing".
          3 := "Certificate Chain too long".
          4 := "Error storing certificate"."""},

    'IMPORT_RES': {
        'data':['count', 'no_user_id', 'imported', 'imported_rsa', 'unchanged',
            'n_uids', 'n_subk', 'n_sigs', 'n_revoc', 'sec_read', 'sec_imported',
        'sec_dups', 'skipped_new_keys', 'not_imported'],
        'msg':"Final statistics on import process."},
    'FILE_START': {
        'data':['what', 'filename'],
        'msg':
"""Start processing a file <filename>.
    <what> indicates the performed operation:
        1 - verify
        2 - encrypt
        3 - decrypt"""},

    'FILE_DONE': {
        'data':[],
        'msg':"Marks the end of a file processing which has been started by FILE_START."},
    'BEGIN_DECRYPTION': {
        'data':[],
        'msg':
"""Mark the start of the actual decryption process.
These are also emitted when in --list-only mode."""},

    'END_DECRYPTION': {
        'data':[],
        'msg':
"""Mark the end of the actual decryption process.
These are also emitted when in --list-only mode."""},

    'BEGIN_ENCRYPTION': {
        'data':['mdc_method', 'sym_algo'],
        'msg':"Mark the start of the actual encryption process."},
    'END_ENCRYPTION': {
        'data':[],
        'msg':"Mark the end of the actual encryption process."},
    'BEGIN_SIGNING': {
        'data':[],
        'msg':"Mark the start of the actual signing process."},

    'DELETE_PROBLEM': {
        'data':['reason_code'],
        'msg':
"""Deleting a key failed. Reason codes are:
        1 - No such key
        2 - Must delete secret key first
        3 - Ambigious specification"""},

    'PROGRESS': {
        'data':['what', 'char', 'cur', 'total'],
        'msg':
"""Used by the primegen and Public key functions to indicate progress.
"char" is the character displayed with no --status-fd enabled, with
    the linefeed replaced by an 'X'.  "cur" is the current amount
    done and "total" is amount to be done; a "total" of 0 indicates that
    the total amount is not known.  The condition TOATL && CUR == TOTAL
    may be used to detect the end of an operation.
    Well known values for WHAT:
        "pk_dsa"   - DSA key generation
        "pk_elg"   - Elgamal key generation
        "primegen" - Prime generation
        "need_entropy" - Waiting for new entropy in the RNG
        "file:XXX" - processing file XXX
                     (note that current gpg versions leave out the
                     "file:" prefix).
        "tick"     - generic tick without any special meaning - useful
                     for letting clients know that the server is
                     still working.
        "starting_agent" - A gpg-agent was started because it is
                           not running as a daemon.
        "learncard" Send by the agent and gpgsm while learing
                    the data of a smartcard.
        "card_busy" A smartcard is still working"""},

    'SIG_CREATED': {
        'data':['type', 'pubkey algo', 'hash algo', 'class',
            'timestamp', 'key fpr'],
        'msg':
"""A signature has been created using these parameters.
    type:  'D' = detached
           'C' = cleartext
           'S' = standard
           (only the first character should be checked)
   class:  2 hex digits with the signature class"""},

    'KEY_CREATED': {
        'data':['type', 'fingerprint', '[handle]'],
        'msg':
"""A key has been created
    type: 'B' = primary and subkey
          'P' = primary
          'S' = subkey"""},

    'KEY_NOT_CREATED': {
        'data':['[handle]'],
        'msg':"The key from batch run has not been created due to errors."},
    'SESSION_KEY': {
        'data':['algo', 'hexdigits'],
        'msg':"The session key used to decrypt the message."},
    'NOTATION_NAME': {
        'data':['name'],
        'msg':"name and string are %XX escaped; the data may be split among several NOTATION_DATA lines."},
    'NOTATION_DATA': {
        'data':['string'],
        'msg':"Data assoiciated with the preceeding 'NOTATION_NAME'"},
    'USERID_HINT': {
        'data':['long-main-keyid', 'string'],
        'msg':"Give a hint about the user ID for a certain keyID."},
    'POLICY_URL': {
        'data':['string'],
        'msg':""},
    'BEGIN_STREAM': {
        'data':[],
        'msg':"Issued by pipemode."},
    'END_STREAM': {
        'data':[],
        'msg':"Issued by pipemode."},
    'INV_RECP': {
        'data':['reason', 'requested_recipient'],
        'msg':
"""Issued for each unusable recipient/sender.
The reasons codes currently in use are:
    0 := "No specific reason given".
    1 := "Not Found"
    2 := "Ambigious specification"
    3 := "Wrong key usage"
    4 := "Key revoked"
    5 := "Key expired"
    6 := "No CRL known"
    7 := "CRL too old"
    8 := "Policy mismatch"
    9 := "Not a secret key"
    10 := "Key not trusted"
    11 := "Missing certificate"
    12 := "Missing issuer certificate"""},

    'INV_SGNR': {
        'data':['reason', 'requested_sender'],
        'msg':
"""Issued for each unusable recipient/sender.
The reasons codes currently in use are:
    0 := "No specific reason given".
    1 := "Not Found"
    2 := "Ambigious specification"
    3 := "Wrong key usage"
    4 := "Key revoked"
    5 := "Key expired"
    6 := "No CRL known"
    7 := "CRL too old"
    8 := "Policy mismatch"
    9 := "Not a secret key"
    10 := "Key not trusted"
    11 := "Missing certificate"
    12 := "Missing issuer certificate"""},

    'NO_RECP': {
        'data':['reserved',],
        'msg':"Issued when no recipients are usable."},
    'NO_SGNR': {
        'data':['reserved'],
        'msg':"Issued when no senders are usable."},
    'ALREADY_SIGNED': {
        'data':['long-keyid'],
        'msg':"Warning: This is experimental and might be removed at any time."},
    'TRUNCATED': {
        'data':['maxno'],
        'msg':"The output was truncated to MAXNO items."},
    'ERROR': {
        'data':['error-location', 'error-code', '[more]'],
        'msg':"This is a generic error status message, it might be followed by error location specific data."},
    'SUCCESS': {
        'data':['[location]'],
        'msg':"Postive confirimation that an operation succeeded."},
    'ATTRIBUTE': {
        'data':['fpr', 'octets', 'type', 'index', 'count',
            'timestamp', 'expiredate', 'flags'],
        'msg':"This is one long line issued for each attribute subpacket when an attribute packet is seen during key listing."},
    'CARDCTRL': {
        'data':['what', '[serialno]'],
        'msg':
"""This is used to control smartcard operations.
    Defined values for WHAT are:
        1 = Request insertion of a card.  Serialnumber may be given
            to request a specific card.  Used by gpg 1.4 w/o scdaemon.
        2 = Request removal of a card.  Used by gpg 1.4 w/o scdaemon.
        3 = Card with serialnumber detected
        4 = No card available.
        5 = No card reader available
        6 = No card support available"""},

    'PLAINTEXT':  {
        'data':['format', 'timestamp', 'filename'],
        'msg':"This indicates the format of the plaintext that is about to be written."},
    'PLAINTEXT_LENGTH':  {
        'data':['length'],
        'msg':"This indicates the length of the plaintext that is about to be written."},
    'SIG_SUBPACKET': {
        'data':['type', 'flags',
            'length', 'data'],
        'msg':"This indicates that a signature subpacket was seen."},
    'SC_OP_FAILURE': {
        'data':['[code]'],
        'msg':
"""An operation on a smartcard definitely failed.
    Defined values for CODE are:
        0 - unspecified error (identically to a missing CODE)
        1 - canceled
        2 - bad PIN"""},

    'SC_OP_SUCCESS': {
        'data':[],
        'msg':"A smart card operaion succeeded."},
    'BACKUP_KEY_CREATED': {
        'data':['fingerprint', 'fname'],
        'msg':"A backup key named FNAME has been created for the key with KEYID."},
    'MOUNTPOINT': {
        'data':['name'],
        'msg':"NAME is a percent-plus escaped filename describing the mountpoint for the current operation (e.g. g13 --mount)."},
    'DECRYPTION_INFO': {
        'data':['mdc_method', 'sym_algo'],
        'msg':"Print information about the symmetric encryption algorithm and the MDC method."},
}

