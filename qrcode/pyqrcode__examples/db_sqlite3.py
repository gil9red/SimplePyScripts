#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3

# pip install pyqrcode
# pip install pypng
import pyqrcode


with sqlite3.connect(":memory:") as connect:
    items = connect.execute("SELECT 'Version: ' || sqlite_version(), date()").fetchone()
    print(items)
    # ('Version: 3.29.0', '2020-07-20')

text = "\n".join(items)

qr_code = pyqrcode.create(text)
qr_code.png("sqlite3.png", scale=6)
