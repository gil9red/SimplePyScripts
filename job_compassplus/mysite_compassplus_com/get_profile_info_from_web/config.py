#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


DIR = Path(__file__).resolve().parent

DB_DIR_NAME: Path = DIR / "database"
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

DB_FILE_NAME: Path = DB_DIR_NAME / "db.sqlite"

DIR_DB_BACKUP: Path = DIR / "database-backup"
DIR_DB_BACKUP.mkdir(parents=True, exist_ok=True)

MAX_LAST_CHECK_DATE_DAYS: int = 30
