#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
from pathlib import Path


DB_FILE_NAME = str(Path(__file__).resolve().parent / "database.sqlite")


def create_connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE_NAME)


def init_db():
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.execute(
            """\
            CREATE TABLE IF NOT EXISTS File (
                id INTEGER PRIMARY KEY,
                file_name TEXT NOT NULL UNIQUE
            );
        """
        )


init_db()
