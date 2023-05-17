#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/827397/5909792


import win32api


def get_drivers() -> list[str]:
    drives_str = win32api.GetLogicalDriveStrings()
    return [item[0] for item in drives_str.split("\x00") if item]


if __name__ == "__main__":
    drives = get_drivers()
    print(drives)
