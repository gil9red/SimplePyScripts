#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from db import create_connect


DIR_NAME = r"C:\\"


with create_connect() as connect:
    sql = "INSERT OR IGNORE INTO File (file_name) VALUES (?)"
    nums = 0

    for file_name in Path(DIR_NAME).rglob("*.png"):
        file_name = str(file_name)
        last_row_id = connect.execute(sql, [file_name]).lastrowid

        nums += bool(last_row_id)

    print(f"Added files: {nums}")
