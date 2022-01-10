#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys

from pathlib import Path


DIR = Path(__file__).resolve().parent
LOGIN_PASSWORD_FILE_NAME = DIR / 'LOGIN_PASSWORD.txt'

try:
    LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD') or LOGIN_PASSWORD_FILE_NAME.read_text('utf-8').strip()
    if not LOGIN_PASSWORD:
        raise Exception('LOGIN_PASSWORD пустой!')

    LOGIN, PASSWORD = LOGIN_PASSWORD.splitlines()
    if not LOGIN or not PASSWORD:
        raise Exception('LOGIN или PASSWORD пустые!')

except:
    print(f'Нужно в {LOGIN_PASSWORD_FILE_NAME.name} или в переменную окружения LOGIN_PASSWORD добавить логин и пароль')
    LOGIN_PASSWORD_FILE_NAME.touch()
    sys.exit()
