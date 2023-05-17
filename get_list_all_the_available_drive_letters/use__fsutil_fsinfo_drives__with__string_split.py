#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os


def get_drivers() -> list[str]:
    text = os.popen("fsutil fsinfo drives").read().strip()
    return [x[0] for x in text.split()[1:]]


if __name__ == "__main__":
    drives = get_drivers()
    print(drives)
