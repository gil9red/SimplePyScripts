#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3


with sqlite3.connect(":memory:") as connect:
    version = connect.execute("SELECT SQLITE_VERSION()").fetchone()[0]
    print(f"SQLite version: {version}")
    # SQLite version: 3.35.5
