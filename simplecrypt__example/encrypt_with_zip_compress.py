#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import binascii
import hashlib
import io
import logging
import random
import string
import sys
import time
import zipfile

from simplecrypt import encrypt, decrypt


def encrypt(password, message, use_zip=False):
    if use_zip:
        zip_data_io = io.BytesIO()

        # Append as data in file
        with zipfile.ZipFile(
            zip_data_io, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zf:
            zf.writestr("message.txt", message)

        message = zip_data_io.getvalue()

    message = encrypt(password, message)
    return message


def decrypt(password, message, use_zip=False):
    message = decrypt(password, message)

    if use_zip:
        zip_data_io = io.BytesIO(message)

        with zipfile.ZipFile(zip_data_io, mode="r") as zf:
            message = zf.read("message.txt")

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


log = get_logger("encrypt_with_zip_compress")


def run_crypt_decrypt(message, password, use_zip=False, show_hex=False):
    start_time = time.time()

    text_hex = binascii.hexlify(message)
    message_digest = get_digest(message)
    log.debug(f"Message len: {len(message)}, digest: {message_digest}")
    show_hex and log.debug(f'text_hex: "{text_hex}"')
    log.debug("")

    log.debug("Encrypt...")
    encrypt_text = encrypt(password, message, use_zip)
    encrypt_text_hex = binascii.hexlify(encrypt_text)
    encrypt_message_digest = get_digest(encrypt_text)
    log.debug(
        f"Encrypt message len: {len(encrypt_text)}, digest: {encrypt_message_digest}"
    )
    show_hex and log.debug(f'encrypt_text_hex: "{encrypt_text_hex}"')

    log.debug("")
    log.debug("Decrypt...")
    decrypt_text = decrypt(password, encrypt_text, use_zip)
    decrypt_text_hex = binascii.hexlify(decrypt_text)
    decrypt_message_digest = get_digest(decrypt_text)
    log.debug(
        f"Decrypt message len: {len(decrypt_text)}, digest: {decrypt_message_digest}"
    )
    show_hex and log.debug(f'decrypt_text_hex: "{decrypt_text_hex}"')

    log.debug("")
    log.debug(f"Digest is equal: {message_digest == decrypt_message_digest}")
    log.debug(f"Total time: {time.time() - start_time:.3f} seconds")


# Random message
MESSAGE = "".join(random.choice(string.hexdigits) for _ in range(5000000)).encode()
PASSWORD = "secret"


if __name__ == "__main__":
    log.debug("CRYPT_DECRYPT_TEST: use_zip=False")
    run_crypt_decrypt(MESSAGE, PASSWORD, use_zip=False)

    log.debug("")
    log.debug("_" * 100)
    log.debug("")

    log.debug("CRYPT_DECRYPT_TEST: use_zip=True")
    run_crypt_decrypt(MESSAGE, PASSWORD, use_zip=True)
