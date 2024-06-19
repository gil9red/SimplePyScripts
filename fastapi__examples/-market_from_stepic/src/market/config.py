#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from pathlib import Path


DIR: Path = Path(__file__).resolve().parent

DB_DIR_NAME: Path = DIR / "database"
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

DB_FILE_NAME: Path = DB_DIR_NAME / "db.shelve"

SECRET_KEY_FILE_NAME = DIR / "SECRET_KEY.txt"
SECRET_KEY = (
    os.environ.get("SECRET_KEY")
    or SECRET_KEY_FILE_NAME.read_text("utf-8").strip()
)
if not SECRET_KEY:
    raise Exception("SECRET_KEY must be set in the SECRET_KEY.txt file or in an environment variable")

ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
