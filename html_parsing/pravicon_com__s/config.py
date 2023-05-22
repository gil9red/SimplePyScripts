#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


DIR = Path(__file__).resolve().parent

DIR_DUMP = DIR / "DUMP_pravicon_com__s"
DIR_DUMP.mkdir(parents=True, exist_ok=True)

FILE_NAME_IDS = DIR / "IDS"

URL_MODIX_BASE, URL_MODIX_CREATE, URL_MODIX_UPDATE, LOGIN, PASSWORD = (
    (DIR / "URL_LOGIN_PASSWORD.txt").read_text("utf-8").strip().splitlines()
)
