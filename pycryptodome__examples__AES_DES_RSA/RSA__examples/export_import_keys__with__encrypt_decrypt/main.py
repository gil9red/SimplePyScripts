#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Для импорта rsa
import sys

sys.path.append("..")
import rsa


FILE_NAME_PUBLIC_KEY = "public.pem"
FILE_NAME_PRIVATE_KEY = "private.pem"


with open(FILE_NAME_PUBLIC_KEY, "rb") as f:
    public_pem = f.read()

with open(FILE_NAME_PRIVATE_KEY, "rb") as f:
    private_pem = f.read()

if public_pem and private_pem:
    public_key = rsa.import_key(public_pem)
    private_key = rsa.import_key(private_pem)

else:
    print(
        f"The {repr(FILE_NAME_PUBLIC_KEY)} or {repr(FILE_NAME_PRIVATE_KEY)} files are empty! "
        f"Performing key generation!"
    )

    public_key, private_key = rsa.new_keys(key_size=2048)
    print("Key generation completed successfully!")

    with open(FILE_NAME_PUBLIC_KEY, "wb") as f:
        f.write(public_key.exportKey("PEM"))

    with open(FILE_NAME_PRIVATE_KEY, "wb") as f:
        f.write(private_key.exportKey("PEM"))

    print("Successfully save generated keys to files!")
    print()


print("private:", private_key.exportKey("PEM"))
print("public:", public_key.exportKey("PEM"))
print()

text = "Hello World!".encode("utf-8")
encrypted = rsa.encrypt(text, public_key)
print(encrypted)

decrypted = rsa.decrypt(encrypted, private_key)
print(decrypted)

assert text == decrypted
