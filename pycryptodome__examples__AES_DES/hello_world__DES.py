#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/Legrandin/pycryptodome


# pip install pycryptodome
# OR:
# pip install pycryptodomex


from Crypto.Cipher import DES

key = b'abcdefgh'


def pad(text):
    while len(text) % 8 != 0:
        text += b' '

    return text


des = DES.new(key, DES.MODE_ECB)
text = b'Hello World!'
padded_text = pad(text)

encrypted_text = des.encrypt(padded_text)
print(encrypted_text)  # b'\x95\x123.Y\x8dN\x17\xcc\xf1\xc7\\\xc7\xac\xbc\x7f'

data = des.decrypt(encrypted_text)
print(data)  # b'Hello World!    '

data = data.rstrip(b' ')
print(data)  # b'Hello World!'
