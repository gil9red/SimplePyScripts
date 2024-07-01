#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from pathlib import Path

# pip install filelock==3.15.4
from filelock import FileLock, Timeout


FILE_NAME = Path(__file__).resolve()
FILE_NAME_LOCK = str(FILE_NAME) + ".lock"


if __name__ == "__main__":
    def main():
        print("Start")
        time.sleep(20)
        print("Finish")

    try:
        with FileLock(FILE_NAME_LOCK, timeout=0):
            main()
    except Timeout:
        print("Detected launch of second application. Shutting down")
