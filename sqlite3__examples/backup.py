#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
import zipfile

from datetime import date
from pathlib import Path

from root_config import DIR_DB


DIR_DB_BACKUP = DIR_DB / "backup"
DIR_DB_BACKUP.mkdir(parents=True, exist_ok=True)

FILE_NAME = Path(__file__).resolve()


def create_zip_for_file(
        file_name_zip: str | Path,
        file_name: Path,
        delete_file_name: bool = True,
):
    with zipfile.ZipFile(file_name_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
        f.write(file_name, arcname=file_name.name)

    if delete_file_name:
        file_name.unlink()


def backup(
        connect: sqlite3.Connection,
        file_name: Path,
        zip: bool = True,
        delete_file_name_after_zip: bool = True,
) -> Path:
    if file_name.exists():
        file_name.unlink()

    connect.execute("VACUUM INTO ?", (str(file_name),))

    if zip:
        file_name_zip = Path(f"{file_name}.zip")
        create_zip_for_file(file_name_zip, file_name, delete_file_name=delete_file_name_after_zip)
        return file_name_zip

    return file_name


def _process_test(connect: sqlite3.Connection):
    connect.executescript(
        """
        create table if not exists stocks (
            date text, 
            trans text, 
            symbol text,
            qty real,
            price real
        );

        insert into stocks values ('2006-01-05', 'BUY', 'RHAT', 100, 35.14);
        insert into stocks values ('2006-05-01', 'BUY', 'TFAR', 40, 112.10);
    """
    )

    print()
    print(connect.execute("select * from stocks").fetchall())
    print()


with sqlite3.connect(":memory:") as connect:
    _process_test(connect)

    file_name_backup = DIR_DB_BACKUP / f"{FILE_NAME.stem}_memory_{date.today()}.db"
    file_name_backup_zip = backup(connect, file_name_backup)
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
