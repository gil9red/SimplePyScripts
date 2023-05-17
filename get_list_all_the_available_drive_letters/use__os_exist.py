#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/34187346/5909792


import os
import string


def get_drivers() -> list[str]:
    return [d for d in string.ascii_uppercase if os.path.exists("%s:" % d)]


if __name__ == "__main__":
    drives = get_drivers()
    print(drives)
