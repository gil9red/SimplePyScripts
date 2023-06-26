#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import binascii

# pip install simple-crypt
# https://github.com/andrewcooke/simple-crypt
from simplecrypt import encrypt, decrypt


message = "Hello World!"
password = "secret"

print('message: "{}"'.format(message))
print('password: "{}"'.format(password))
print()

ciphertext = encrypt(password, message)
print('ciphertext[{}]: "{}"'.format(len(ciphertext), ciphertext))

ciphertext_hex = binascii.hexlify(ciphertext)
print('ciphertext_hex[{}]: "{}"'.format(len(ciphertext_hex), ciphertext_hex))
print()

print("After decrypt:")
plaintext = decrypt(password, ciphertext)
print(plaintext)
