#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3

from datetime import date
from pathlib import Path

from config import DIR_DB, DIR_DB_BACKUP
from common import create_zip_for_file, _process_test


FILE_NAME = Path(__file__).resolve()


def backup(
        connect: sqlite3.Connection,
        file_name: Path,
        zip: bool = True,
        delete_file_name_after_zip: bool = True,
) -> Path:
    dst = sqlite3.connect(file_name)
    connect.backup(dst)
    dst.close()

    if zip:
        file_name_zip = Path(f"{file_name}.zip")
        create_zip_for_file(file_name_zip, file_name, delete_file_name=delete_file_name_after_zip)
        return file_name_zip

    return file_name


with sqlite3.connect(":memory:") as connect:
    _process_test(connect)

    file_name_backup = DIR_DB_BACKUP / f"{FILE_NAME.stem}_memory_{date.today()}.db"
    file_name_backup_zip = backup(connect, file_name_backup, delete_file_name_after_zip=False)
    print(f"Создан бэкап базы данных в: {file_name_backup_zip}")


with sqlite3.connect(
        str(DIR_DB / FILE_NAME.stem) + ".db",
        isolation_level=None,
) as connect:
    connect.execute('pragma journal_mode=wal')

    _process_test(connect)

    file_name_backup = DIR_DB_BACKUP / f"{FILE_NAME.stem}_wal_{date.today()}.db"
    file_name_backup_zip = backup(connect, file_name_backup)
    print(f"Создан бэкап базы данных в: {file_name_backup_zip}")
