#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pycryptodome
# OR:
# pip install pycryptodomex
from Crypto.PublicKey import RSA


SECRET_CODE = "Unguessable"

key = RSA.generate(2048)
encrypted_key = key.export_key(passphrase=SECRET_CODE)
print(key.publickey().export_key())

# READ
key = RSA.import_key(encrypted_key, passphrase=SECRET_CODE)
print(key.publickey().export_key())
