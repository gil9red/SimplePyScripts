#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
from pathlib import Path

from config import DIR_DB, DIR_DB_BACKUP
from common import create_zip_for_file, run_test


FILE_NAME = Path(__file__).resolve()


def backup(
        connect: sqlite3.Connection,
        file_name: Path,
        use_zip: bool = True,
        delete_file_name_after_zip: bool = True,
) -> Path:
    dst = sqlite3.connect(file_name)
    connect.backup(dst)
    dst.close()

    if use_zip:
        file_name_zip = Path(f"{file_name}.zip")
        create_zip_for_file(file_name_zip, file_name, delete_file_name=delete_file_name_after_zip)
        return file_name_zip

    return file_name


run_test(
    backup=backup,
    file_name=FILE_NAME,
    dir_db=DIR_DB,
    dir_db_backup=DIR_DB_BACKUP,
    # NOTE:
    # use_zip: bool = True,
    # delete_file_name_after_zip: bool = True,
)
