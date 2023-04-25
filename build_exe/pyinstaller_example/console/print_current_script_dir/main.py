#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# FROM: https://github.com/gil9red/SimplePyScripts/blob/927af3d3f05a0129338b21d074ca241c8a055118/get_current_script_dir.py


import inspect
import os
import sys


def get_current_script_dir(follow_symlinks=True, normcase=False) -> str:
    # py2exe, PyInstaller, cx_Freeze
    if getattr(sys, "frozen", False):
        path = os.path.abspath(sys.executable)
    else:
        # Analog inspect.getabsfile without os.path.normcase
        path = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.abspath(path)

    if follow_symlinks:
        path = os.path.realpath(path)

    if normcase:
        path = os.path.normcase(path)

    return os.path.dirname(path)


if __name__ == "__main__":
    print(get_current_script_dir())
