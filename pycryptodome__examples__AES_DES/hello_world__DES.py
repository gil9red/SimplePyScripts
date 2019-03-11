#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/Legrandin/pycryptodome


# pip install pycryptodome
# OR:
# pip install pycryptodomex


from Crypto.Cipher import DES


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/99ec5746cc93c8f1c143af0a04a42716d3dc5a16/pycryptodome__examples__AES_DES/info_security.py
def pad(s: bytes, bs=8) -> bytes:
    return s + bytes((bs - len(s) % bs) for _ in range(bs - len(s) % bs))


def unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]


key = b'abcdefgh'


des = DES.new(key, DES.MODE_ECB)
text = b'Hello World!'
padded_text = pad(text)

encrypted_text = des.encrypt(padded_text)
print(encrypted_text)  # b'\x95\x123.Y\x8dN\x17\xcc\xf1\xc7\\\xc7\xac\xbc\x7f'

data = des.decrypt(encrypted_text)
print(data)  # b'Hello World!\x04\x04\x04\x04'

data = unpad(data)
print(data)  # b'Hello World!'
