#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import shutil
import sqlite3

from datetime import datetime
from pathlib import Path

# pip install pillow
from PIL import Image

# pip install imagehash
import imagehash


DB_FILE_NAME = str(Path(__file__).resolve().parent / "database.sqlite")


def create_connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE_NAME)


def init_db() -> None:
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.execute(
            """\
            CREATE TABLE IF NOT EXISTS ImageHash (
                id INTEGER PRIMARY KEY,
                file_name TEXT NOT NULL UNIQUE,
                average_hash TEXT NOT NULL,
                phash TEXT NOT NULL,
                phash_simple TEXT NOT NULL,
                dhash TEXT NOT NULL,
                dhash_vertical TEXT NOT NULL,
                whash TEXT NOT NULL,
                colorhash TEXT NOT NULL
            );
            """
        )


def db_add(
    file_name: str,
    average_hash: str,
    phash: str,
    phash_simple: str,
    dhash: str,
    dhash_vertical: str,
    whash: str,
    colorhash: str,
) -> bool:
    sql = """\
        INSERT OR IGNORE INTO ImageHash (
            file_name, 
            average_hash,
            phash,
            phash_simple,
            dhash,
            dhash_vertical,
            whash,
            colorhash
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    file_name = str(Path(file_name).resolve())

    with create_connect() as connect:
        last_row_id = connect.execute(
            sql,
            [
                file_name,
                average_hash,
                phash,
                phash_simple,
                dhash,
                dhash_vertical,
                whash,
                colorhash,
            ],
        ).lastrowid

        # True, if successful
        return bool(last_row_id)


def db_add_image(file_name: str) -> bool:
    image = Image.open(file_name)
    return db_add(
        file_name,
        str(imagehash.average_hash(image)),
        str(imagehash.phash(image)),
        str(imagehash.phash_simple(image)),
        str(imagehash.dhash(image)),
        str(imagehash.dhash_vertical(image)),
        str(imagehash.whash(image)),
        str(imagehash.colorhash(image)),
    )


def db_exists(file_name: str) -> bool:
    sql = "SELECT 1 FROM ImageHash WHERE file_name = ?"
    file_name = str(Path(file_name).resolve())

    with create_connect() as connect:
        return bool(connect.execute(sql, [file_name]).fetchone())


def db_get_all() -> list[dict]:
    with create_connect() as connect:
        connect.row_factory = sqlite3.Row

        return connect.execute("SELECT * FROM ImageHash").fetchall()


def db_create_backup(backup_dir="backup") -> None:
    file_name = str(datetime.today().date()) + ".sqlite"
    os.makedirs(backup_dir, exist_ok=True)

    file_name = os.path.join(backup_dir, file_name)
    shutil.copy(DB_FILE_NAME, file_name)


init_db()


if __name__ == "__main__":
    print(len(db_get_all()))
