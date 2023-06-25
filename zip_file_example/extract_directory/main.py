#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


DIR_NAME = "dir_1"


if __name__ == "__main__":
    import zipfile

    with zipfile.ZipFile(DIR_NAME + ".zip", mode="r") as zf:
        zf.extractall()
