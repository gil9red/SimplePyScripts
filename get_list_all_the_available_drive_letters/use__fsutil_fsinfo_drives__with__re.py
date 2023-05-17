#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import re


def get_drivers() -> list[str]:
    text = os.popen("fsutil fsinfo drives").read().strip()
    return re.findall(r"([A-Z]):\\", text)


if __name__ == "__main__":
    drives = get_drivers()
    print(drives)
