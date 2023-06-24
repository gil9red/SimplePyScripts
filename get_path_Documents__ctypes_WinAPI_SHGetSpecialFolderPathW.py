#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
import sys

from ctypes.wintypes import MAX_PATH


# SOURCE: https://github.com/mhammond/pywin32/blob/d64fac8d7bda2cb1d81e2c9366daf99e802e327f/com/win32comext/shell/shellcon.py#L284
CSIDL_PERSONAL = 5


shell32 = ctypes.windll.shell32
buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
if not shell32.SHGetSpecialFolderPathW(None, buf, CSIDL_PERSONAL, False):
    # This buf.value is empty
    print("Failure!")
    sys.exit()

print(buf.value)
# C:\Users\ipetrash\Documents
