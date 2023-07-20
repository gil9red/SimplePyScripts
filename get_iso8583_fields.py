#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def get_iso8583_fields(hex_str: str) -> list[int]:
    binary = ""
    for i in range(0, len(hex_str), 2):
        b = bin(int(hex_str[i : i + 2], 16))[2:].zfill(8)
        binary += b

    return [num for num, flag in enumerate(binary, 1) if flag == "1"]


if __name__ == "__main__":
    text_hex = "02300100008000000000000000000000"
    assert get_iso8583_fields(text_hex) == [7, 11, 12, 24, 41]

    text_hex = "E000000000000000E000000000000001"
    assert get_iso8583_fields(text_hex) == [1, 2, 3, 65, 66, 67, 128]
