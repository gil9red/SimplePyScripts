#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Data Compression (модуль zlib_example)
import zlib


text = b"witch which has which witches wrist watch"
print(f"[{len(text)}]: {text} (crc32: {zlib.crc32(text)})")

print()
print("Compress...")
compress_text = zlib.compress(text)
print(f"[{len(compress_text)}]: {compress_text} (crc32: {zlib.crc32(compress_text)})")

print()
print("Decompress...")

decompress_text = zlib.decompress(compress_text)
print(
    f"[{len(decompress_text)}]: {decompress_text} (crc32: {zlib.crc32(decompress_text)})"
)
