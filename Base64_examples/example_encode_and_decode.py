#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64

text = "Hello py! Привет py!"
print(f"Text: {text}")

b16 = base64.b16encode(text.encode())
b32 = base64.b32encode(text.encode())
b64 = base64.b64encode(text.encode())
b85 = base64.b85encode(text.encode())

print("encode(base16): '%s'" % b16)
print("encode(base32): '%s'" % b32)
print("encode(base64): '%s'" % b64)
print("encode(base85): '%s'" % b85)

print()
print("decode(base16): '%s'" % base64.b16decode(b16))
print("decode(base32): '%s'" % base64.b32decode(b32))
print("decode(base64): '%s'" % base64.b64decode(b64))
print("decode(base85): '%s'" % base64.b85decode(b85))

print()
print("decode(base16) utf-8: '%s'" % base64.b16decode(b16).decode())
print("decode(base32) utf-8: '%s'" % base64.b32decode(b32).decode())
print("decode(base64) utf-8: '%s'" % base64.b64decode(b64).decode())
print("decode(base85) utf-8: '%s'" % base64.b85decode(b85).decode())
