#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"

import sqlite3
import zipfile
from pathlib import Path


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
