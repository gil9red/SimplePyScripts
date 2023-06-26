#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib
import io
import zipfile

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

    print("Compress message in zip...")
    zip_data_io = io.BytesIO()

    # # Append as file
    # with zipfile.ZipFile(zip_data, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
    #     zf.write(FILENAME)

    # Append as data in file
    with zipfile.ZipFile(zip_data_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(FILENAME, message)

    zip_data = zip_data_io.getvalue()
    zip_data_digest = get_digest(zip_data)
    print("Zip len: {}, digest: {}".format(len(zip_data), zip_data_digest))

    # # Save memory zip in file
    # open(FILENAME + '.zip', 'wb').write(data)

    print()
    print("Encrypt zip...")
    cipher_zip_data = encrypt(PASSWORD, zip_data)
    cipher_zip_digest = get_digest(cipher_zip_data)
    print(
        "Encrypt zip len: {}, digest: {}".format(
            len(cipher_zip_data), cipher_zip_digest
        )
    )

    print()
    print("_" * 100)
    print()

    print("Decrypt zip...")
    decrypt_zip_data = decrypt(PASSWORD, cipher_zip_data)
    zip_data_io = io.BytesIO(decrypt_zip_data)
    decrypt_zip_data_digest = get_digest(decrypt_zip_data)
    print(
        "Decrypt zip len: {}, digest: {}".format(
            len(decrypt_zip_data), decrypt_zip_data_digest
        )
    )

    print()
    print("Decompress message from zip...")
    with zipfile.ZipFile(zip_data_io, mode="r") as zf:
        decompress_message = zf.read(FILENAME)

    decompress_message_digest = get_digest(decompress_message)
    print(
        "Decompress message len: {}, digest: {}".format(
            len(decompress_message), decompress_message_digest
        )
    )

    print()
    print("_" * 100)
    print()

    print()
    print(
        "Digest for zip is equal: {}".format(zip_data_digest == decrypt_zip_data_digest)
    )
    print(
        "Digest for message is equal: {}".format(
            message_digest == decompress_message_digest
        )
    )
