#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
import random

from timeit import default_timer, timeit


with sqlite3.connect(":memory:") as c:
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT,
            trans TEXT,
            symbol TEXT,
            qty REAL,
            price REAL
        )
        """
    )

    print("Generate items...")
    t = default_timer()
    purchases = [
        (
            random.choice(["2006-03-28", "2006-04-05", "2006-04-06"]),
            random.choice(["SELL", "BUY"]),
            random.choice(["IBM", "MSFT"]),
            random.choice([500, 1000, 600]),
            random.choice([53.00, 45.00, 72.00]),
        )
        for _ in range(500_000)
    ]
    print(f"Elapsed {default_timer() - t:.3f} secs")
    # Elapsed 0.754 secs

    print()

    print("INSERT INTO...")
    t = default_timer()
    c.executemany("INSERT INTO stocks VALUES (NULL, ?, ?, ?, ?, ?)", purchases)
    c.commit()
    print(f"Elapsed {default_timer() - t:.3f} secs")
    # Elapsed 0.484 secs

    print()

    print("SELECT COUNT DEFAULT UPPER...")
    sql = "SELECT COUNT(*) FROM stocks WHERE UPPER(trans) LIKE UPPER('%SELL%')"
    elapsed = timeit(
        stmt="c.execute(sql).fetchone()",
        globals=dict(sql=sql, c=c),
        number=100,
    )
    print(f"Elapsed {elapsed:.3f} secs")
    # Elapsed 7.677 secs

    print()

    c.create_function("upper", narg=1, func=str.upper)

    print("SELECT COUNT PYTHON UPPER...")
    sql = "SELECT COUNT(*) FROM stocks WHERE UPPER(trans) LIKE UPPER('%SELL%')"
    elapsed = timeit(
        stmt="c.execute(sql).fetchone()",
        globals=dict(sql=sql, c=c),
        number=100,
    )
    print(f"Elapsed {elapsed:.3f} secs")
    # Elapsed 18.656 secs
