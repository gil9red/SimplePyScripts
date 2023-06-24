#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random


def get_random_hex_color():
    return "".join(random.choices("0123456789ABCDEF", k=6))


if __name__ == "__main__":
    print(get_random_hex_color())
