#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import binascii
import hashlib
import logging
import random
import string
import sys
import time
import zlib

from simplecrypt import encrypt, decrypt


def encrypt(password, message, use_zlib=False):
    if use_zlib:
        message = zlib.compress(message)

    message = encrypt(password, message)
    return message


def decrypt(password, message, use_zlib=False):
    message = decrypt(password, message)

    if use_zlib:
        message = zlib.decompress(message)

    return message


def get_digest(data):
    sha1 = hashlib.sha1(data)
    return sha1.hexdigest()


def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(message)s")

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


log = get_logger("encrypt_with_zlib_compress")


def crypt_decrypt_test(message, password, use_zlib=False, show_hex=False):
    start_time = time.time()

    text_hex = binascii.hexlify(message)
    message_digest = get_digest(message)
    log.debug("Message len: {}, digest: {}".format(len(message), message_digest))
    show_hex and log.debug('text_hex: "{}"'.format(text_hex))
    log.debug("")

    log.debug("Encrypt...")
    encrypt_text = encrypt(password, message, use_zlib)
    encrypt_text_hex = binascii.hexlify(encrypt_text)
    encrypt_message_digest = get_digest(encrypt_text)
    log.debug(
        "Encrypt message len: {}, digest: {}".format(
            len(encrypt_text), encrypt_message_digest
        )
    )
    show_hex and log.debug('encrypt_text_hex: "{}"'.format(encrypt_text_hex))

    log.debug("")
    log.debug("Decrypt...")
    decrypt_text = decrypt(password, encrypt_text, use_zlib)
    decrypt_text_hex = binascii.hexlify(decrypt_text)
    decrypt_message_digest = get_digest(decrypt_text)
    log.debug(
        "Decrypt message len: {}, digest: {}".format(
            len(decrypt_text), decrypt_message_digest
        )
    )
    show_hex and log.debug('decrypt_text_hex: "{}"'.format(decrypt_text_hex))

    log.debug("")
    log.debug("Digest is equal: {}".format(message_digest == decrypt_message_digest))
    log.debug("Total time: {:.3f} seconds".format(time.time() - start_time))


# Random message
MESSAGE = "".join(random.choice(string.hexdigits) for _ in range(5000000)).encode()
PASSWORD = "secret"


if __name__ == "__main__":
    log.debug("CRYPT_DECRYPT_TEST: use_zlib=False")
    crypt_decrypt_test(MESSAGE, PASSWORD, use_zlib=False)

    log.debug("")
    log.debug("_" * 100)
    log.debug("")

    log.debug("CRYPT_DECRYPT_TEST: use_zlib=True")
    crypt_decrypt_test(MESSAGE, PASSWORD, use_zlib=True)
