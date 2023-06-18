#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import os


FILE_NAME_RUN = "__temporary_run.bat"
TEXT_RUN = """\
@echo off
set PYTHONPATH=custom/path/to/modules;custom/path/to/modules2
start {python} -c "import sys;print(sys.path);import time;time.sleep(50)"
"""
TEXT_RUN = TEXT_RUN.format(python=sys.executable)


if __name__ == "__main__":
    with open(FILE_NAME_RUN, mode="w") as f:
        f.write(TEXT_RUN)

    os.system(FILE_NAME_RUN)
    os.remove(FILE_NAME_RUN)
