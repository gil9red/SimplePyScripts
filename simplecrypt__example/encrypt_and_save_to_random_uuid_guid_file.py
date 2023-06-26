#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import binascii
import uuid

from simplecrypt import encrypt


message = "Hello World!"
password = "secret"

print('message: "{}"'.format(message))
print('password: "{}"'.format(password))
print()

encrypt_text = encrypt(password, message)
print('encrypt_text[{}]: "{}"'.format(len(encrypt_text), encrypt_text))

encrypt_text_hex = binascii.hexlify(encrypt_text)
print('encrypt_text_hex[{}]: "{}"'.format(len(encrypt_text_hex), encrypt_text_hex))
print()

# Random uuid
file_name = str(uuid.uuid4())
print("Save to file:", file_name)

with open(file_name, mode="wb") as f:
    f.write(encrypt_text)
