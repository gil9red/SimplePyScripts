#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


DIR = Path(__file__).resolve().parent.parent

DIR_DB = DIR / "databases"
DIR_DB.mkdir(parents=True, exist_ok=True)

DIR_DB_BACKUP = DIR_DB / "backup"
DIR_DB_BACKUP.mkdir(parents=True, exist_ok=True)
