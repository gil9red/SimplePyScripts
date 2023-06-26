#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import binascii

# pip install simple-crypt
# https://github.com/andrewcooke/simple-crypt
from simplecrypt import encrypt, decrypt


message = "Hello World!"
password = "secret"

print(f'message: "{message}"')
print(f'password: "{password}"')
print()

ciphertext = encrypt(password, message)
print(f'ciphertext[{len(ciphertext)}]: "{ciphertext}"')

ciphertext_hex = binascii.hexlify(ciphertext)
print(f'ciphertext_hex[{len(ciphertext_hex)}]: "{ciphertext_hex}"')
print()

print("After decrypt:")
plaintext = decrypt(password, ciphertext)
print(plaintext)
