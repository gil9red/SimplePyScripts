#!/usr/bin/env python
#
# Decompressor/compressor for files in Mozilla's "mozLz4" format. Firefox uses this file format to
# compress e. g. bookmark backups (*.jsonlz4).
#
# This file format is in fact just plain LZ4 data with a custom header (magic number [8 bytes] and
# uncompressed file size [4 bytes, little endian]).
#
# This Python 3 script requires the LZ4 bindings for Python, see: https://pypi.python.org/pypi/lz4
#
#
# Copyright (c) 2015, Tilman Blumenbach
# Copyright (c) 2021, Ilya Petrash
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of
#    conditions and the following disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# SOURCE: https://gist.githubusercontent.com/Tblue/62ff47bef7f894e92ed5/raw/2483756c55ed34be565aea269f05bd5eeb6b0a33/mozlz4a.py


import json
import sys

from typing import BinaryIO

# pip install lz4
import lz4.block


class MozLz4aError(Exception):
    pass


class InvalidHeader(MozLz4aError):
    pass


HEADER_MAGIC_NUMBER = b"mozLz40\0"


def decompress(file_obj: BinaryIO) -> bytes:
    return decompress_data(file_obj.read())


def compress(file_obj: BinaryIO) -> bytes:
    return compress_data(file_obj.read())


def decompress_data(data: bytes) -> bytes:
    if data[:8] != HEADER_MAGIC_NUMBER:
        raise InvalidHeader("Invalid magic number")

    return lz4.block.decompress(data[8:])


def compress_data(data: bytes) -> bytes:
    compressed = lz4.block.compress(data)
    return HEADER_MAGIC_NUMBER + compressed


def loads_json(file_obj: BinaryIO) -> dict:
    data = decompress(file_obj)
    return json.loads(data)


def dumps_json(file_obj: BinaryIO, json_data: dict):
    data = json.dumps(json_data).encode("utf-8")
    compressed = compress_data(data)

    file_obj.write(compressed)


if __name__ == "__main__":
    from argparse import ArgumentParser

    argparser = ArgumentParser(description="MozLz4a compression/decompression utility")
    argparser.add_argument(
        "-d",
        "--decompress",
        "--uncompress",
        action="store_true",
        help="Decompress the input file instead of compressing it.",
    )
    argparser.add_argument("in_file", help="Path to input file.")
    argparser.add_argument("out_file", help="Path to output file.")

    parsed_args = argparser.parse_args()

    try:
        in_file = open(parsed_args.in_file, "rb")
    except IOError as e:
        print(
            "Could not open input file `%s' for reading: %s" % (parsed_args.in_file, e),
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        out_file = open(parsed_args.out_file, "wb")
    except IOError as e:
        print(
            "Could not open output file `%s' for writing: %s"
            % (parsed_args.out_file, e),
            file=sys.stderr,
        )
        sys.exit(3)

    try:
        if parsed_args.decompress:
            data = decompress(in_file)
        else:
            data = compress(in_file)
    except Exception as e:
        print(
            "Could not compress/decompress file `%s': %s" % (parsed_args.in_file, e),
            file=sys.stderr,
        )
        sys.exit(4)

    try:
        out_file.write(data)
    except IOError as e:
        print(
            "Could not write to output file `%s': %s" % (parsed_args.out_file, e),
            file=sys.stderr,
        )
        sys.exit(5)
    finally:
        out_file.close()
