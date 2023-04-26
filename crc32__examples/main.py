#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import zlib


def crc32_from_bytes(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def crc32_hex_from_bytes(data: bytes) -> str:
    return "%08X" % crc32_from_bytes(data)


def crc32_hex_from_file(filename):
    with open(filename, "rb") as f:
        buf = f.read()

    return crc32_hex_from_bytes(buf)


if __name__ == "__main__":
    print(crc32_from_bytes(b"hello-world"))  # 2983461467
    print(crc32_hex_from_bytes(b"hello-world"))  # B1D4025B
    print()
    print(crc32_hex_from_file("1.csv"))  # 7EB0F2B2
    print(crc32_hex_from_file("2.csv"))  # 5D884C77
