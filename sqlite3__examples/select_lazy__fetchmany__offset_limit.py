#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/43493784/5909792


import sqlite3


def _print_1(c: sqlite3.Cursor) -> None:
    i = 1
    while True:
        batch = c.fetchmany(BATCH_SIZE)
        if not batch:
            break

        print(f"{i:3}. {len(batch):3}: {batch}")
        i += 1


def _print_2(c: sqlite3.Cursor) -> None:
    for i, batch in enumerate(iter(lambda: c.fetchmany(BATCH_SIZE), []), 1):
        print(f"{i:3}. {len(batch):3}: {batch}")


def _print_3(c: sqlite3.Cursor, sql: str) -> None:
    i = 1
    offset = 0
    while True:
        c.execute(sql + " LIMIT ? OFFSET ?", (BATCH_SIZE, offset))
        batch = list(c)
        offset += BATCH_SIZE
        if not batch:
            break

        print(f"{i:3}. {len(batch):3}: {batch}")
        i += 1


connect = sqlite3.connect(":memory:")

connect.execute(
    """\
    CREATE TABLE IF NOT EXISTS Foo (
        id INTEGER PRIMARY KEY,
        number INTEGER NOT NULL UNIQUE
    );
"""
)

# Fill
connect.executemany(
    "INSERT OR IGNORE INTO Foo (number) VALUES (?)", ((i,) for i in range(999))
)
print(connect.execute("SELECT COUNT(*) FROM Foo").fetchone()[0])
# 999

print()

BATCH_SIZE = 100
sql = "SELECT number FROM Foo"

c = connect.cursor()

c.execute(sql)
_print_1(c)

print("\n" + "-" * 100 + "\n")

c.execute(sql)
_print_2(c)

print("\n" + "-" * 100 + "\n")

_print_3(c, sql)
