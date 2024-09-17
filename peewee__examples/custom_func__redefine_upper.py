#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from peewee import SqliteDatabase


def run_sql(connect):
    print(connect.execute("""SELECT "ы", UPPER("ы") """).fetchone())
    print(connect.execute("""SELECT "s", UPPER("s") """).fetchone())
    print(connect.execute("""SELECT 1 WHERE UPPER("ы") LIKE UPPER("Ы") """).fetchone())
    print(connect.execute("""SELECT 1 WHERE "ы" LIKE "Ы" """).fetchone())
    print(connect.execute("""SELECT 1 WHERE "s" LIKE "S" """).fetchone())


def db_func():
    print("[db_func]")

    db = SqliteDatabase(":memory:")
    db.connect()

    with db.connection() as connect:
        run_sql(connect)
        """
        ('ы', 'ы')
        ('s', 'S')
        None
        None
        (1,)
        """

    print()

    @db.func("upper")
    def upper(value: str) -> str | None:
        if value is None:
            return
        return value.upper()

    with db.connection() as connect:
        run_sql(connect)
        """
        ('ы', 'Ы')
        ('s', 'S')
        (1,)
        None
        (1,)
        """


def db_create_function():
    print("[db_create_function]")

    db = SqliteDatabase(":memory:")
    db.connect()

    with db.connection() as connect:
        run_sql(connect)
        """
        ('ы', 'ы')
        ('s', 'S')
        None
        None
        (1,)
        """

        print()
        connect.create_function("upper", narg=1, func=str.upper)

        run_sql(connect)
        """
        ('ы', 'Ы')
        ('s', 'S')
        (1,)
        None
        (1,)
        """


db_create_function()

print()

db_func()
