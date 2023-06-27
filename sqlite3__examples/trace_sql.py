#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3


with sqlite3.connect(":memory:") as connect:
    my_print = lambda text: print("SQL: " + text.strip())
    connect.set_trace_callback(my_print)
    # OR:
    # connect.set_trace_callback(print)

    print(connect.execute("SELECT sqlite_version();").fetchone())

    print()
    connect.executescript(
        """\
    CREATE TABLE Test (
        id INTEGER PRIMARY KEY, 
        name TEXT
    );

    INSERT INTO Test (name) VALUES ('One');
    INSERT INTO Test (name) VALUES ('Two');
    INSERT INTO Test (name) VALUES ('Three');
    """
    )

    print()
    connect.execute("INSERT INTO Test (name) VALUES (?);", ("Four",))

    print()
    connect.execute("INSERT INTO Test (name) VALUES (:name);", {"name": "Five"})

    print()
    print(connect.execute("select * from Test;").fetchall())
    print()

    connect.commit()
