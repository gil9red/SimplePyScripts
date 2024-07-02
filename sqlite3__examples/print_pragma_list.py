#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3


with sqlite3.connect(":memory:") as connect:
    cursor = connect.execute("PRAGMA pragma_list")
    for i, (name, ) in enumerate(cursor, 1):
        print(f"{i}. {name!r}")
    """
    1. 'analysis_limit'
    2. 'application_id'
    3. 'auto_vacuum'
    4. 'automatic_index'
    5. 'busy_timeout'
    ...
    62. 'trusted_schema'
    63. 'user_version'
    64. 'wal_autocheckpoint'
    65. 'wal_checkpoint'
    66. 'writable_schema'
    """

    print("\n" + "-" * 100 + "\n")

    cursor = connect.execute("SELECT * FROM pragma_pragma_list")
    for i, (name, ) in enumerate(cursor, 1):
        print(f"{i}. {name!r}")
    """
    1. 'analysis_limit'
    2. 'application_id'
    3. 'auto_vacuum'
    4. 'automatic_index'
    5. 'busy_timeout'
    ...
    62. 'trusted_schema'
    63. 'user_version'
    64. 'wal_autocheckpoint'
    65. 'wal_checkpoint'
    66. 'writable_schema'
    """
