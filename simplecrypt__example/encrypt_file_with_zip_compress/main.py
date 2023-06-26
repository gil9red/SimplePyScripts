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
    print(f"Message len: {len(message)}, digest: {message_digest}")

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
    print(f"Zip len: {len(zip_data)}, digest: {zip_data_digest}")

    # # Save memory zip in file
    # open(FILENAME + '.zip', 'wb').write(data)

    print()
    print("Encrypt zip...")
    cipher_zip_data = encrypt(PASSWORD, zip_data)
    cipher_zip_digest = get_digest(cipher_zip_data)
    print(
        f"Encrypt zip len: {len(cipher_zip_data)}, digest: {cipher_zip_digest}"
    )

    print()
    print("_" * 100)
    print()

    print("Decrypt zip...")
    decrypt_zip_data = decrypt(PASSWORD, cipher_zip_data)
    zip_data_io = io.BytesIO(decrypt_zip_data)
    decrypt_zip_data_digest = get_digest(decrypt_zip_data)
    print(
        f"Decrypt zip len: {len(decrypt_zip_data)}, digest: {decrypt_zip_data_digest}"
    )

    print()
    print("Decompress message from zip...")
    with zipfile.ZipFile(zip_data_io, mode="r") as zf:
        decompress_message = zf.read(FILENAME)

    decompress_message_digest = get_digest(decompress_message)
    print(
        f"Decompress message len: {len(decompress_message)}, digest: {decompress_message_digest}"
    )

    print()
    print("_" * 100)
    print()

    print()
    print(
        f"Digest for zip is equal: {zip_data_digest == decrypt_zip_data_digest}"
    )
    print(
        f"Digest for message is equal: {message_digest == decompress_message_digest}"
    )
