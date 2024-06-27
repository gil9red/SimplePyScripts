#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys

from pathlib import Path


DIR = Path(__file__).resolve().parent

TOKEN_FILE_NAME = DIR / "TOKEN.txt"
SEP = "|"

try:
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        TOKEN = TOKEN_FILE_NAME.read_text("utf-8").strip()
    if not TOKEN:
        raise Exception("TOKEN пустой!")

    USERNAME, PASSWORD = TOKEN.split(SEP)

except:
    print(
        f"Нужно в {TOKEN_FILE_NAME.name} или в переменную окружения "
        f"TOKEN добавить логин/пароль (формат <домен>\\<логин>{SEP}<пароль>)"
    )
    TOKEN_FILE_NAME.touch()
    sys.exit()
