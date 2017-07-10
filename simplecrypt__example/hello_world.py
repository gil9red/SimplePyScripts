#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


message = 'Hello World!'
password = 'secret'

print('message: "{}"'.format(message))
print('password: "{}"'.format(password))
print()

from simplecrypt import encrypt, decrypt
ciphertext = encrypt(password, message)
print('ciphertext: "{}"'.format(ciphertext))

import binascii
ciphertext_hex = binascii.hexlify(ciphertext)
print('ciphertext_hex: "{}"'.format(ciphertext_hex))
print()

print('After decrypt:')
plaintext = decrypt(password, ciphertext)
print(plaintext)
