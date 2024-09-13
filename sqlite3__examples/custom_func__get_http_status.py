#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
import requests


def get_http_status(url: str) -> int:
    return requests.get(url).status_code


with sqlite3.connect(":memory:") as connect:
    connect.create_function("get_http_status", narg=1, func=get_http_status)

    print(connect.execute("""SELECT get_http_status("https://ya.ru") """).fetchone()[0])
    # 200

    print(connect.execute("""SELECT get_http_status("https://ya.ru/404") """).fetchone()[0])
    # 404
