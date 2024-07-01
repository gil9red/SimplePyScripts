#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
import zipfile

from datetime import date
from pathlib import Path
from typing import Callable


def create_zip_for_file(
        file_name_zip: str | Path,
        file_name: Path,
        delete_file_name: bool = True,
):
    with zipfile.ZipFile(file_name_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as f:
        f.write(file_name, arcname=file_name.name)

    if delete_file_name:
        file_name.unlink()


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

    print(connect.execute("select * from stocks").fetchall())


def run_test(
    backup: Callable,
    file_name: Path,
    dir_db: Path,
    dir_db_backup: Path,
    use_zip: bool = True,
    delete_file_name_after_zip: bool = True,
):
    with sqlite3.connect(":memory:") as connect:
        _process_test(connect)

        file_name_backup = dir_db_backup / f"{file_name.stem}_memory_{date.today()}.db"
        # TODO: use_zip, delete_file_name_after_zip
        file_name_backup_zip = backup(connect, file_name_backup)
        print(f"Создан бэкап базы данных в: {file_name_backup_zip}")

    with sqlite3.connect(
        str(dir_db / file_name.stem) + ".db",
        isolation_level=None,
    ) as connect:
        connect.execute('pragma journal_mode=wal')

        _process_test(connect)

        file_name_backup = dir_db_backup / f"{file_name.stem}_wal_{date.today()}.db"
        # TODO: use_zip, delete_file_name_after_zip
        file_name_backup_zip = backup(connect, file_name_backup)
        print(f"Создан бэкап базы данных в: {file_name_backup_zip}")
