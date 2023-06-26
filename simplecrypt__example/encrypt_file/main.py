#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib

from simplecrypt import encrypt, decrypt


def get_digest(data):
    sha1 = hashlib.sha1(data)
    return sha1.hexdigest()


PASSWORD = "secret"
FILENAME = "message.txt"


if __name__ == "__main__":
    print("Reading message...")
    with open("message.txt", mode="rb") as f:
        message = f.read()

    message_digest = get_digest(message)
    print("Message len: {}, digest: {}".format(len(message), message_digest))

    print()
    print("Encrypt message...")
    cipher_text = encrypt(PASSWORD, message)
    print("Encrypt message len: {}".format(len(cipher_text)))

    with open(FILENAME + ".crypto", mode="wb") as f:
        f.write(cipher_text)

    print("")
    print("_" * 100)
    print("")

    print()
    print("Decrypt message...")

    with open(FILENAME + ".crypto", mode="rb") as f:
        cipher_text = f.read()

    decrypt_message = decrypt(PASSWORD, cipher_text)
    decrypt_message_digest = get_digest(decrypt_message)
    print(
        "Decrypt message len: {}, digest: {}".format(
            len(decrypt_message), decrypt_message_digest
        )
    )

    print()
    print("Digest is equal: {}".format(message_digest == decrypt_message_digest))
