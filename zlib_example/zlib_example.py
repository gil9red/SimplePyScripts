#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Data Compression (модуль zlib_example)
import zlib

text = b'witch which has which witches wrist watch'
print('[{}]: {} (crc32: {})'.format(len(text), text, zlib.crc32(text)))

print()
print('Compress...')
compress_text = zlib.compress(text)
print('[{}]: {} (crc32: {})'.format(len(compress_text), compress_text, zlib.crc32(compress_text)))

print()
print('Decompress...')

decompress_text = zlib.decompress(compress_text)
print('[{}]: {} (crc32: {})'.format(len(decompress_text), decompress_text, zlib.crc32(decompress_text)))
