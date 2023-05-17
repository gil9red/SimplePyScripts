#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/827398/5909792


import string
from ctypes import windll


def get_drivers() -> list[str]:
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()

    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


if __name__ == "__main__":
    drives = get_drivers()
    print(drives)
