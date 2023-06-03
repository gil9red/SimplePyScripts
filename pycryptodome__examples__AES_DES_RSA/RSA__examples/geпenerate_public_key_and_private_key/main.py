#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/Legrandin/pycryptodome/blob/29810b96cefc900138523203f027a179a15ceffe/Doc/src/examples.rst#generate-public-key-and-private-key


# pip install pycryptodome
# OR:
# pip install pycryptodomex
from Crypto.PublicKey import RSA


key = RSA.generate(2048)
print(key)  # Private RSA key at...

private_key = key.export_key()
print(private_key)  # b'-----BEGIN RSA PRIVATE KEY-----\n...

with open("private.pem", "wb") as f:
    f.write(private_key)

public_key = key.publickey().export_key()
print(public_key)  # b'-----BEGIN PUBLIC KEY-----\nMIIBIj...

with open("public.pem", "wb") as f:
    f.write(public_key)
