#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://stackoverflow.com/a/22881871/5909792


import inspect
import os
import sys


def get_script_dir(follow_symlinks=True) -> str:
    # py2exe, PyInstaller, cx_Freeze
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)

    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)


if __name__ == '__main__':
    print(get_script_dir())
