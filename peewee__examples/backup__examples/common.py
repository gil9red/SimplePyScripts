#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
from pathlib import Path
from typing import Callable

# pip install peewee
from peewee import Model, SqliteDatabase, TextField


db = SqliteDatabase("db.sqlite")


class Info(Model):
    first_name = TextField()
    second_name = TextField()

    class Meta:
        database = db

    @classmethod
    def fill(cls):
        count = cls.select().count()
        for i in range(5):
            cls.create(
                first_name=f"first_name_{i + count}",
                second_name=f"second_name_{i + count}",
            )

    @classmethod
    def print(cls):
        for info in cls.select():
            print(info)

    @classmethod
    def print_from(cls, file_name: str | Path):
        connection = sqlite3.connect(file_name)
        try:
            for info in connection.execute(f"SELECT * FROM {cls._meta.table_name}"):
                print(info)
        except Exception as e:
            print(f"[#] {e}")

    def __str__(self):
        return f"Info<#{self.id} first_name={self.first_name!r} second_name={self.second_name!r}>"


def run_test(
    backup: Callable,
    file_name_backup: Path | str,
):
    print("[db backup] Print:")
    Info.print_from(file_name_backup)
    print()

    Info.fill()

    print("[db] After fill:")
    Info.print()

    backup(db, file_name_backup)


db.connect()
db.create_tables([Info])


if __name__ == "__main__":
    Info.fill()

    Info.print()
    """
    Info<#1 first_name='first_name_0' second_name='second_name_0'>
    Info<#2 first_name='first_name_1' second_name='second_name_1'>
    Info<#3 first_name='first_name_2' second_name='second_name_2'>
    Info<#4 first_name='first_name_3' second_name='second_name_3'>
    Info<#5 first_name='first_name_4' second_name='second_name_4'>
    """

    Info.print_from("db.sqlite")
    """
    (1, 'first_name_0', 'second_name_0')
    (2, 'first_name_1', 'second_name_1')
    (3, 'first_name_2', 'second_name_2')
    (4, 'first_name_3', 'second_name_3')
    (5, 'first_name_4', 'second_name_4')
    """
