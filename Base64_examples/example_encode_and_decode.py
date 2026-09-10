#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64


text: str = "Hello py! Привет py!"
data: bytes = text.encode()
print(f"Text ({len(text)}): {text!r}")
print(f"Data ({len(data)}): {data!r}")
"""
Text (20): 'Hello py! Привет py!'
Data (26): b'Hello py! \xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82 py!'
"""

print()

b16: bytes = base64.b16encode(data)
b32: bytes = base64.b32encode(data)
b64: bytes = base64.b64encode(data)
b85: bytes = base64.b85encode(data)

print(f"encode base16 ({len(b16)}): {b16!r}")
print(f"encode base32 ({len(b32)}): {b32!r}")
print(f"encode base64 ({len(b64)}): {b64!r}")
print(f"encode base85 ({len(b85)}): {b85!r}")
"""
encode base16 (52): b'48656C6C6F2070792120D09FD180D0B8D0B2D0B5D18220707921'
encode base32 (48): b'JBSWY3DPEBYHSIJA2CP5DAGQXDILFUFV2GBCA4DZEE======'
encode base64 (36): b'SGVsbG8gcHkhINCf0YDQuNCy0LXRgiBweSE='
encode base85 (33): b'NM&qnZy<1aAt2D7(SXpn(6Z3A(Sjgwc_9'
"""

assert base64.b16decode(b16) == data
assert base64.b16decode(b16) == data
assert base64.b16decode(b16) == data
assert base64.b16decode(b16) == data
