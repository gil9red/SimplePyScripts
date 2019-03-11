#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/713f8b9c4f607b4016c2b1d3209084c752691460/pycryptodome__examples__AES_DES/info_security.py#L38
def pad(s: bytes, bs=8) -> bytes:
    pad_size = bs - (len(s) % bs)
    return s + bytes([pad_size] * pad_size)


def unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]


if __name__ == '__main__':
    data = b'Hello'
    padded_data = pad(data)
    print(padded_data)                         # b'Hello\x03\x03\x03'
    print(unpad(padded_data))                  # b'Hello'
    print(unpad(padded_data).decode('utf-8'))  # Hello

    print()

    data = 'Привет!'.encode('utf-8')
    padded_data = pad(data)
    print(padded_data)         # b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82!\x03\x03\x03'
    print(unpad(padded_data))  # b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82!'
    print(unpad(padded_data).decode('utf-8'))  # Привет!
