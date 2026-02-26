#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
from pathlib import Path

from peewee import SqliteDatabase


def backup(db: SqliteDatabase, file_name: Path | str) -> None:
    dst = sqlite3.connect(file_name)
    db.connection().backup(dst)
    dst.close()


if __name__ == "__main__":
    from common import run_test

    run_test(
        backup=backup,
        file_name_backup=Path(__file__).resolve().name + ".db",
    )
