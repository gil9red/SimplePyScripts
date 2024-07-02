#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3

# pip install tabulate
from tabulate import tabulate


with sqlite3.connect(":memory:") as connect:
    sql_table = "pragma_function_list"

    # NOTE: "PRAGMA function_list" == "SELECT * FROM pragma_function_list"
    columns = [row[1] for row in connect.execute(f"PRAGMA table_info({sql_table})")]
    print(columns)
    # ['name', 'builtin', 'type', 'enc', 'narg', 'flags']

    cursor = connect.execute(f"SELECT * FROM {sql_table}")
    rows = (
        [i, *row]
        for i, row in enumerate(cursor, 1)
    )
    print(tabulate(rows, headers=["#"] + columns, tablefmt="grid"))
    """
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    |   # | name                      |   builtin | type   | enc   |   narg |   flags |
    +=====+===========================+===========+========+=======+========+=========+
    |   1 | pow                       |         1 | s      | utf8  |      2 | 2099200 |
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    |   2 | group_concat              |         1 | w      | utf8  |      1 | 2097152 |
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    |   3 | group_concat              |         1 | w      | utf8  |      2 | 2097152 |
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    ...
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    | 149 | fts5_source_id            |         0 | s      | utf8  |      0 |       0 |
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    | 150 | offsets                   |         0 | s      | utf8  |      1 |       0 |
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    | 151 | fts5_rowid                |         0 | s      | utf8  |     -1 |       0 |
    +-----+---------------------------+-----------+--------+-------+--------+---------+
    """
