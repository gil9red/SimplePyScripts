#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import struct


msg = struct.pack(">I12s", 12, b"Hello World!")
print(msg)  # b'\x00\x00\x00\x0cHello World!'
print()

data = struct.unpack(">I12s", msg)
print(data)  # (12, b'Hello World!')

data = struct.unpack(">I12s", b"\x00\x00\x00\x0cHello World!")
print(data)  # (12, b'Hello World!')
