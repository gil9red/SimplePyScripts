#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from peewee import SqliteDatabase


db = SqliteDatabase(":memory:")


@db.func("get_http_status")
def get_http_status(url: str) -> int:
    return requests.get(url).status_code


db.connect()

with db.connection() as connect:
    print(connect.execute("""SELECT get_http_status("https://ya.ru") """).fetchone()[0])
    # 200

    print(connect.execute("""SELECT get_http_status("https://ya.ru/404") """).fetchone()[0])
    # 404
