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
    print(f"Message len: {len(message)}, digest: {message_digest}")

    print()
    print("_" * 100)
    print()

    print("Compress message...")
    compress_text = zlib.compress(message)
    compress_message_digest = get_digest(compress_text)
    print(
        f"Compress message len: {len(compress_text)}, digest: {compress_message_digest}"
    )

    print()
    print("Encrypt compress message...")
    cipher_compress_text = encrypt(PASSWORD, compress_text)
    print(f"Encrypt compress message len: {len(cipher_compress_text)}")

    print()
    print("_" * 100)
    print()

    print("Decrypt compress message...")
    decrypt_compress_message = decrypt(PASSWORD, cipher_compress_text)
    decrypt_compress_message_digest = get_digest(decrypt_compress_message)
    print(
        f"Decrypt compress message len: {len(decrypt_compress_message)}, digest: {decrypt_compress_message_digest}"
    )

    print()
    print("Decompress message...")
    decompress_text = zlib.decompress(decrypt_compress_message)
    decompress_message_digest = get_digest(decompress_text)
    print(
        f"Decompress message len: {len(decompress_text)}, digest: {decompress_message_digest}"
    )

    print()
    print("_" * 100)
    print()

    print()
    print(
        f"Digest for compress is equal: {compress_message_digest == decrypt_compress_message_digest}"
    )
    print(
        f"Digest for message is equal: {message_digest == decompress_message_digest}"
    )
