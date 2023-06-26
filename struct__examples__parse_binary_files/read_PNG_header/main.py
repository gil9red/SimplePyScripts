#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
# SOURCE: https://en.wikipedia.org/wiki/Portable_Network_Graphics#File_format


import glob
import struct

import zlib


def crc32_from_bytes(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def print_info(file_name: str):
    print(file_name)

    def read_chunk(f) -> (int, bytes, bytes, int):
        chunk_length, = struct.unpack('>I', f.read(4))
        chunk_type = f.read(4)
        chunk_data = f.read(chunk_length)
        chunk_CRC, = struct.unpack('>I', f.read(4))

        return chunk_length, chunk_type, chunk_data, chunk_CRC

    with open(file_name, 'rb') as f:
        # HEADER
        data = f.read(8)

        if data != b'\x89PNG\r\n\x1a\n':
            print('Not valid PNG!')
            return

        # After the header comes a series of chunks, each of which conveys certain information about the image.

        # A chunk consists of four parts: length (4 bytes, big-endian), chunk type/name (4 bytes),
        # chunk data (length bytes) and CRC (cyclic redundancy code/checksum; 4 bytes). The CRC is
        # a network-byte-order CRC-32 computed over the chunk type and chunk data, but not the length.
        #   | Length  | Chunk type | Chunk data    | CRC     |
        #   | 4 bytes | 4 bytes    | Length bytes  | 4 bytes |

        # Need IHDR chunk:
        # IHDR must be the first chunk; it contains (in this order) the image's width (4 bytes),
        # height (4 bytes), bit depth (1 byte), color type (1 byte), compression method (1 byte),
        # filter method (1 byte), and interlace method (1 byte) (13 data bytes total).

        chunk_length, chunk_type, chunk_data, chunk_CRC = read_chunk(f)
        # print(chunk_length, chunk_type, chunk_data, chunk_CRC)

        # Check CRC
        assert crc32_from_bytes(chunk_type + chunk_data) == chunk_CRC

        width, \
        height, \
        bit_depth, \
        color_type, \
        compression_method, \
        filter_method, \
        interlace_method = struct.unpack('>IIbbbbb', chunk_data)
        print(f'    Size: {width}x{height}')


if __name__ == '__main__':
    for file_name in glob.glob('*.png'):
        print_info(file_name)
        print()
