#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib
import zlib

from simplecrypt import encrypt, decrypt


def get_digest(data):
    sha1 = hashlib.sha1(data)
    return sha1.hexdigest()


PASSWORD = "secret"
FILENAME = "message.txt"


if __name__ == "__main__":
    print("Reading message...")
    message = open("message.txt", mode="rb").read()
    message_digest = get_digest(message)
    print("Message len: {}, digest: {}".format(len(message), message_digest))

    print()
    print("_" * 100)
    print()

    print("Compress message...")
    compress_text = zlib.compress(message)
    compress_message_digest = get_digest(compress_text)
    print(
        "Compress message len: {}, digest: {}".format(
            len(compress_text), compress_message_digest
        )
    )

    print()
    print("Encrypt compress message...")
    cipher_compress_text = encrypt(PASSWORD, compress_text)
    print("Encrypt compress message len: {}".format(len(cipher_compress_text)))

    print()
    print("_" * 100)
    print()

    print("Decrypt compress message...")
    decrypt_compress_message = decrypt(PASSWORD, cipher_compress_text)
    decrypt_compress_message_digest = get_digest(decrypt_compress_message)
    print(
        "Decrypt compress message len: {}, digest: {}".format(
            len(decrypt_compress_message), decrypt_compress_message_digest
        )
    )

    print()
    print("Decompress message...")
    decompress_text = zlib.decompress(decrypt_compress_message)
    decompress_message_digest = get_digest(decompress_text)
    print(
        "Decompress message len: {}, digest: {}".format(
            len(decompress_text), decompress_message_digest
        )
    )

    print()
    print("_" * 100)
    print()

    print()
    print(
        "Digest for compress is equal: {}".format(
            compress_message_digest == decrypt_compress_message_digest
        )
    )
    print(
        "Digest for message is equal: {}".format(
            message_digest == decompress_message_digest
        )
    )
