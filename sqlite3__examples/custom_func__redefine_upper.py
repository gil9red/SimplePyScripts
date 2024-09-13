#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3


with sqlite3.connect(":memory:") as connect:
    print(connect.execute("""SELECT "ы", UPPER("ы") """).fetchone())
    print(connect.execute("""SELECT "s", UPPER("s") """).fetchone())
    print(connect.execute("""SELECT 1 WHERE UPPER("ы") LIKE UPPER("Ы") """).fetchone())
    print(connect.execute("""SELECT 1 WHERE "ы" LIKE "Ы" """).fetchone())
    print(connect.execute("""SELECT 1 WHERE "s" LIKE "S" """).fetchone())
    """
    ('ы', 'ы')
    ('s', 'S')
    None
    None
    (1,)
    """

    print()
    connect.create_function("upper", narg=1, func=str.upper)

    print(connect.execute("""SELECT "ы", UPPER("ы") """).fetchone())
    print(connect.execute("""SELECT "s", UPPER("s") """).fetchone())
    print(connect.execute("""SELECT 1 WHERE UPPER("ы") LIKE UPPER("Ы") """).fetchone())
    print(connect.execute("""SELECT 1 WHERE "ы" LIKE "Ы" """).fetchone())
    print(connect.execute("""SELECT 1 WHERE "s" LIKE "S" """).fetchone())
    """
    ('ы', 'Ы')
    ('s', 'S')
    (1,)
    None
    (1,)
    """
