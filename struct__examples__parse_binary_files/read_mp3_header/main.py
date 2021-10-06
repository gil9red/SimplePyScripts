#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://en.wikipedia.org/wiki/List_of_file_signatures
# SOURCE: https://id3.org/id3v2.3.0#ID3v2_header


import struct


def is_id3(data: bytes) -> bool:
    return data[:3] == b'ID3'


def is_mp3(data: bytes) -> bool:
    if is_id3(data):
        return True

    first_2 = data[:2]
    for signature in [b'\xFF\xFB', b'\xFF\xF3', b'\xFF\xF2']:
        if first_2 == signature:
            return True

    return False


if __name__ == '__main__':
    # SimplePyScripts\
    from pathlib import Path
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent

    for file_name in ROOT_DIR.rglob("*.mp3"):
        print(file_name)

        data = file_name.read_bytes()
        _is_mp3 = is_mp3(data)
        _is_id3 = is_id3(data)
        print(f'    IS MP3: {_is_mp3}')
        print(f'    IS ID3: {_is_id3}')
        if _is_id3:
            header = data[:10]

            #  3b      2b      1b     4b
            file_id, version, flags, size = struct.unpack('<3sHB4s', header)
            real_size = int("".join(map(lambda x: bin(x)[2:].zfill(8), size)).replace('0', ''), 2)

            print(f'    ID3.header: {"".join(map(lambda x: hex(x)[2:].zfill(2), header))}')
            print(f'    ID3.file_id: {file_id}')
            print(f'    ID3.version: {version}')
            print(f'    ID3.flags: {bin(flags)[2:].zfill(8)}')
            print(f'    ID3.size: {" ".join(map(lambda x: hex(x)[2:].zfill(2), size))}')
            print(f'    ID3.real_size: {real_size} bytes')

        print()
