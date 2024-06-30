#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from pathlib import Path

from filelock import FileLock, Timeout


FILE_NAME = Path(__file__).resolve()
FILE_NAME_LOCK = str(FILE_NAME) + ".lock"


try:
    with FileLock(FILE_NAME_LOCK, timeout=0):
        print("Lock")
        time.sleep(20)
except Timeout:
    print("Обнаружен запуск второго приложения. Завершение работы")
