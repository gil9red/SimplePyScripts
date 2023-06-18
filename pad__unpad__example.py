#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def pad(s: bytes, bs=8) -> bytes:
    pad_size = bs - (len(s) % bs)
    return s + bytes([pad_size] * pad_size)


def unpad(s: bytes) -> bytes:
    pad_size = s[-1]
    return s[:-pad_size]


if __name__ == "__main__":
    data = b"Hello"
    padded_data = pad(data)
    print(padded_data)  # b'Hello\x03\x03\x03'
    print(unpad(padded_data))  # b'Hello'
    print(unpad(padded_data).decode("utf-8"))  # Hello
    assert data == unpad(pad(data))
    print()

    assert b"123" == unpad(pad(b"123"))
    assert b"123" * 9999 == unpad(pad(b"123" * 9999))
    assert b"11111111" == unpad(pad(b"11111111"))
    assert b"abcd123" == unpad(pad(b"abcd123"))

    print(unpad(b"12\x02\x02"))  # b'12'
    print(unpad(b"1\x01"))  # b'1'
    print()

    data = "Привет!".encode("utf-8")
    padded_data = pad(data)
    print(padded_data)
    # b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82!\x03\x03\x03'
    print(unpad(padded_data))  # b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82!'
    print(unpad(padded_data).decode("utf-8"))  # Привет!
    assert data == unpad(pad(data))
