#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/toddw-as/pyDes


# pip install pyDes
import pyDes


data = b"Hello World!"

# def __init__(self, key, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
k = pyDes.des(
    b"DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5
)

d = k.encrypt(data)
print("Encrypted: %r" % d)
print("Decrypted: %r" % k.decrypt(d))
assert k.decrypt(d) == data
