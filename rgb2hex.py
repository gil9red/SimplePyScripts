#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def rgb2hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


if __name__ == "__main__":
    print(rgb2hex(255, 0, 0))  # #FF0000
    print(rgb2hex(0, 255, 0))  # #00FF00
    print(rgb2hex(0, 0, 255))  # #0000FF
