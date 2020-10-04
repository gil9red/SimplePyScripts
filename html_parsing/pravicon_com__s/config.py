#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path


DIR = Path(__file__).resolve().parent

DIR_DUMP = DIR / 'DUMP_pravicon_com__s'
DIR_DUMP.mkdir(parents=True, exist_ok=True)

URL_MODIX, LOGIN, PASSWORD = (DIR / 'URL_LOGIN_PASSWORD.txt').read_text('utf-8').strip().splitlines()
