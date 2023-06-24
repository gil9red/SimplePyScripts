#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def k_notation_to_number(num_str: str) -> int:
    i = num_str.index("k")
    num, size = num_str[:i], len(num_str[i:])
    return int(float(num) * (1000**size))


if __name__ == "__main__":
    print(k_notation_to_number("1k"))  # 1000
    print(k_notation_to_number("1.5kk"))  # 1500000
    print(k_notation_to_number("1kkk"))  # 1000000000
