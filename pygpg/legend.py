#!/usr/bin/python
# -*- coding: utf-8 -*-
####################
# pyGPG LEGEND
####################
# File:       legend.py
#
#             LEGEND data for interpreting the results
#             of gpg operation status messages
#
# Copyright:
#             (c) 2012 Brian Dolbec
#             Distributed under the terms of the BSD license
#
# Author(s):
#             Brian Dolbec <dolsen@gentoo.org>
#
'''Holds pyGPG's gpg status output legend.'''


from collections import namedtuple

#import snakeoil.klass

# make this global, so is easy to change, and calculates only once
GPG_IDENTIFIER = '[GNUPG:]'
PYGPG_IDENTIFIER = '[PyGPG:]'
GPG_VER_IDENTFIER = 'gpg (GnuPG)'


CLASSES = [
    ('NEWSIG', [], "Issued right before a signature verification starts."),
    ('GOODSIG', ['long_keyid', 'username'], "The signature with the keyid is good."),
    ('EXPSIG', ['long_keyid', 'username'], "The signature with the keyid is good, but the signature is expired."),
    ('EXPKEYSIG', ['long_keyid', 'username'], "The signature with the keyid is good, but the signature was made by an expired key."),
    ('REVKEYSIG', ['long_keyid', 'username'], "The signature with the keyid is good, but the signature was made by a revoked key."),
    ('BADSIG', ['long_keyid', 'username'], "The signature with the keyid has not been verified okay."),
    ('ERRSIG', ['long_keyid', 'pubkey_algo', 'hash_algo', 'sig_class', 'timestamp', 'rc'], "It was not possible to check the signature."),
    ('VALIDSIG', ['fingerprint', 'sig_creation_date', 'sig_timestamp', 'expire_timestamp', 'sig_version', 'reserved', 'pubkey_algo',
        'hash_algo', 'sig_class','primary_key_fpr'], "The signature with the keyid is good."),
    ('SIG_ID', ['radix64_string', 'sig_creation_date', 'sig_timestamp'], "This is emitted only for signatures of class 0 or 1 which have been verified okay."),
    ('ENC_TO', ['long_keyid', 'keytype', 'keylength'], "The message is encrypted to this LONG_KEYID."),
    ('NODATA', ['what'],
"""No data has been found. Codes for what are:
    1 - No armored data.
    2 - Expected a packet but did not found one.
    3 - Invalid packet found, this may indicate a non OpenPGP
            message.
    4 - signature expected but not found
You may see more than one of these status lines."""
    ),
    ('UNEXPECTED', ['what'], "Unexpected data has been encountered, 0 - not further specified"),
    ('TRUST_UNDEFINED', ['error_token'], ""),
    ('TRUST_NEVER', ['error_token'], "For good signatures, this indicates the validity of the key used to create the signature."),
    ('TRUST_MARGINAL', ['validation_model'], "For good signatures, this indicates the validity of the key used to create the signature."),
    ( 'TRUST_FULLY', ['validation_model'], "For good signatures, this indicates the validity of the key used to create the signature."),
    ('TRUST_ULTIMATE', ['validation_model'], "For good signatures, this indicates the validity of the key used to create the signature."),
    ('PKA_TRUST_GOOD', ['mailbox'], "A status code emitted in addition to a TRUST_* status."),
    ('PKA_TRUST_BAD', ['mailbox'], "A status code emitted in addition to a TRUST_* status."),
    ('SIGEXPIRED', [], "This is deprecated in favor of KEYEXPIRED."),
    ('KEYEXPIRED', ['expire_timestamp'], "The key has expired.  expire_timestamp is the expiration time in seconds since Epoch."),
    ('KEYREVOKED', [], "The used key has been revoked by its owner."),
    ('BADARMOR', [], "The ASCII armor is corrupted."),
    ('RSA_OR_IDEA', [], "The IDEA algorithms has been used in the data."),
    ('SHM_INFO', [], ""),
    ('SHM_GET', [], ""),
    ('SHM_GET_BOOL', [], ""),
    ('SHM_GET_HIDDEN', [], ""),
    ('GET_BOOL', [], ""),
    ('GET_LINE', [], ""),
    ('GET_HIDDEN', [], ""),
    ('GOT_IT', [], ""),
    ('NEED_PASSPHRASE', ['long_main_keyid', 'long_keyid', 'keytype', 'keylength'], "Issued whenever a passphrase is needed."),
    ('NEED_PASSPHRASE_SYM', ['cipher_algo', 's2k_mode', 's2k_hash'], "Issued whenever a passphrase for symmetric encryption is needed."),
    ('NEED_PASSPHRASE_PIN', ['card_type', 'chvno', 'serialno'], "Issued whenever a PIN is requested to unlock a card."),
    ('MISSING_PASSPHRASE', [], "No passphrase was supplied."),
    ('BAD_PASSPHRASE', ['long_keyid'], "The supplied passphrase was wrong or not given."),
    ('GOOD_PASSPHRASE', [], "The supplied passphrase was good and the secret key material is therefore usable."),
    ('DECRYPTION_FAILED', [], "The symmetric decryption failed - one reason could be a wrong passphrase for a symmetrical encrypted message."),
    ('DECRYPTION_OKAY', [], "The decryption process succeeded."),
    ('NO_PUBKEY', ['long_keyid'], "The key is not available"),
    ('NO_SECKEY', ['long_keyid'], "The key is not available"),
    ('IMPORT_CHECK', ['long_keyid', 'fingerprint', 'user_ID'], 'This status is emitted in interactive mode right before the "import.okay" prompt.'),
    ('IMPORTED', ['long_keyid', 'username'], "The keyid and name of the signature just imported"),
    ('IMPORT_OK', ['reason', 'fingerprint'],
"""The key with the primary key's FINGERPRINT has been imported.
    Reason flags:
      0 := Not actually changed
      1 := Entirely new key.
      2 := New user IDs
      4 := New signatures
      8 := New subkeys
     16 := Contains private key.
    The flags may be ORed."""
    ),
    ('IMPORT_PROBLEM', ['reason', 'fingerprint'],
"""Issued for each import failure.  Reason codes are:
      0 := "No specific reason given".
      1 := "Invalid Certificate".
      2 := "Issuer Certificate missing".
      3 := "Certificate Chain too long".
      4 := "Error storing certificate"."""
    ),
    ('IMPORT_RES', ['count', 'no_user_id', 'imported', 'imported_rsa', 'unchanged', 'n_uids', 'n_subk', 'n_sigs',
        'n_revoc', 'sec_read', 'sec_imported', 'sec_dups', 'skipped_new_keys', 'not_imported'],
        "Final statistics on import process."
    ),
    ('FILE_START', ['what', 'filename'],
"""Start processing a file <filename>.
    <what> indicates the performed operation:
        1 - verify
        2 - encrypt
        3 - decrypt"""
    ),
    ('FILE_DONE', [], "Marks the end of a file processing which has been started by FILE_START."),
    ('BEGIN_DECRYPTION', [],
"""Mark the start of the actual decryption process.
These are also emitted when in --list-only mode."""
    ),
    ('END_DECRYPTION', [],
"""Mark the end of the actual decryption process.
These are also emitted when in --list-only mode."""
    ),
    ('BEGIN_ENCRYPTION', ['mdc_method', 'sym_algo'], "Mark the start of the actual encryption process."),
    ('END_ENCRYPTION', [], "Mark the end of the actual encryption process."),
    ('BEGIN_SIGNING', ['hash_algo'], "Mark the start of the actual signing process."),
    ('DELETE_PROBLEM', 'reason_code',
"""Deleting a key failed. Reason codes are:
        1 - No such key
        2 - Must delete secret key first
        3 - Ambigious specification"""
    ),
    ('PROGRESS', ['what', 'char', 'cur', 'total'],
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
        "card_busy" A smartcard is still working"""
    ),
    ('SIG_CREATED', ['type', 'pubkey_algo', 'hash_algo', 'sig_class', 'timestamp', 'key_fpr'],
"""A signature has been created using these parameters.
    type:  'D' = detached
           'C' = cleartext
           'S' = standard
           (only the first character should be checked)
   class:  2 hex digits with the signature class"""
    ),
    ('KEY_CREATED', ['type', 'fingerprint', 'handle'],
"""A key has been created
    type: 'B' = primary and subkey
          'P' = primary
          'S' = subkey"""),
    ('KEY_NOT_CREATED', ['handle'], "The key from batch run has not been created due to errors."),
    ('SESSION_KEY', ['algo', 'hexdigits'], "The session key used to decrypt the message."),
    ('NOTATION_NAME', ['name'], "name and string are %XX escaped; the data may be split among several NOTATION_DATA lines."),
    ('NOTATION_DATA', ['string'], "Data assoiciated with the preceeding 'NOTATION_NAME'"),
    ('USERID_HINT', ['long_main_keyid', 'string'], "Give a hint about the user ID for a certain keyID."),
    ('POLICY_URL', ['string'], ""),
    ('BEGIN_STREAM', [], "Issued by pipemode."),
    ('END_STREAM', [], "Issued by pipemode."),
    ('INV_RECP', ['reason', 'requested_recipient'],
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
    12 := "Missing issuer certificate"""
    ),
    ('INV_SGNR', ['reason', 'requested_sender'],
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
    12 := "Missing issuer certificate"""
    ),
    ('NO_RECP', ['reserved'], "Issued when no recipients are usable."),
    ('NO_SGNR', ['reserved'], "Issued when no senders are usable."),
    ('ALREADY_SIGNED', ['long_keyid'], "Warning: This is experimental and might be removed at any time."),
    ('TRUNCATED', ['maxno'], "The output was truncated to MAXNO items."),
    ('ERROR', ['error_location', 'error_code', 'more'], "This is a generic error status message, it might be followed by error location specific data."),
    ('SUCCESS', ['location'], "Postive confirimation that an operation succeeded."),
    ('ATTRIBUTE', ['fpr', 'octets', 'type', 'index', 'count', 'timestamp', 'expiredate', 'flags'],
        "This is one long line issued for each attribute subpacket when an attribute packet is seen during key listing."),
    ('CARDCTRL', ['what', 'serialno'],
"""This is used to control smartcard operations.
    Defined values for WHAT are:
        1 = Request insertion of a card.  Serialnumber may be given
            to request a specific card.  Used by gpg 1.4 w/o scdaemon.
        2 = Request removal of a card.  Used by gpg 1.4 w/o scdaemon.
        3 = Card with serialnumber detected
        4 = No card available.
        5 = No card reader available
        6 = No card support available"""
    ),
    ('PLAINTEXT', ['format', 'timestamp', 'filename'], "This indicates the format of the plaintext that is about to be written."),
    ('PLAINTEXT_LENGTH', ['length'], "This indicates the length of the plaintext that is about to be written."),
    ('SIG_SUBPACKET', ['type', 'flags', 'length', 'data'], "This indicates that a signature subpacket was seen."),
    ('SC_OP_FAILURE', ['code'],
"""An operation on a smartcard definitely failed.
    Defined values for CODE are:
        0 - unspecified error (identically to a missing CODE)
        1 - canceled
        2 - bad PIN"""
    ),
    ('SC_OP_SUCCESS', [], "A smart card operaion succeeded."),
    ('BACKUP_KEY_CREATED', ['fingerprint', 'fname'], "A backup key named FNAME has been created for the key with KEYID."),
    ('MOUNTPOINT', ['name'],"NAME is a percent-plus escaped filename describing the mountpoint for the current operation (e.g. g13 --mount)."),
    ('DECRYPTION_INFO', ['mdc_method', 'sym_algo'], "Print information about the symmetric encryption algorithm and the MDC method."),
    ('GPG_VERSION', ['gpg', 'libcrypt', 'copyright', 'license', 'home', 'sup_pubkey', 'sup_cipher', 'sup_hash', 'sup_compress'],
'''GnuPG version information
    sup_pubkey = supported public key types
    sub_cipher = supported Cipher algorithms
    sup_hash = suppoted Hash algorithms
    sup_compress = supported compression algorithms
''' ),

## PyGPG message classes

    ('PYGPG_VERSION', ['pygpg', 'license'], "PyGPG version information"),
    ('PYGPG_UNEXPECTED_DATA', ['key', 'fields', 'extra_data'], 'Unexpected data was encountered processing a gpg status ouput message'),
    ('PYGPG_ATTRIBUTE_ERROR', ['module', 'classname'], "ERROR retreiving class."),
    ('PYGPG_MESSAGE', ['message'], 'Generic mesage'),
    ('PYGPG_ERROR', ['error', 'function', 'message'], "Internal pyGPG error message, refer to the data's attributes for more detail"),
]


# create the classes

for (name, fields, msg) in CLASSES:
    obj = locals()[name] = namedtuple(name, fields)
    #obj.name = snakeoil.klass.alias_attr('__class__.__name__')
    obj.name = obj.__class__.__name__
    obj.msg = msg
    obj.__slots__ = ()
del obj

