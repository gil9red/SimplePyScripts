#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pycryptodome
# OR:
# pip install pycryptodomex
from Crypto.Cipher import AES

# pip install pkcs7
from pkcs7 import PKCS7Encoder


key = "12647863128053333215894456187814"
mode = AES.MODE_ECB

text = "Hello World!"

encoder = PKCS7Encoder()
pad_text = encoder.encode(text)
print(pad_text)  # "Hello World!"
print(bytes(pad_text, "utf-8"))  # b'Hello World!\x04\x04\x04\x04'

encryptor = AES.new(key, mode)

cipher = encryptor.encrypt(pad_text)
print(cipher)  # b'Hq\x88\xd9\x90\xd8\x8dh\x99\xdf&Z\xe8\xc1\xa9\xe4'

print()

decrypt_text = encryptor.decrypt(cipher)
print(decrypt_text)  # b'Hello World!\x04\x04\x04\x04'

decrypt_text = str(decrypt_text, "utf-8")

unpad_text = encoder.decode(decrypt_text)
print(unpad_text)  # Hello World!
