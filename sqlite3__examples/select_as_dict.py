#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3


with sqlite3.connect(":memory:") as connect:
    connect.executescript(
        """
        create table stocks (
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
    print()

    # SOURCE: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
    # SOURCE: https://docs.python.org/3/library/sqlite3.html#row-objects
    connect.row_factory = sqlite3.Row
    items = connect.execute("select * from stocks").fetchall()
    print(items[0]["symbol"])
    print([dict(x) for x in items])
