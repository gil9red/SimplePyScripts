#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from typing import Iterable

# pip install peewee
from peewee import SqliteDatabase, Model, Field, CharField


class ListField(Field):
    def python_value(self, value: str) -> list:
        return json.loads(value)

    def db_value(self, value: Iterable | None) -> str:
        if value is not None:
            if not isinstance(value, list):
                raise Exception("Type must be a list")

        return json.dumps(value, ensure_ascii=False)


db = SqliteDatabase("db.sqlite", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class KeyByList(BaseModel):
    key = CharField(unique=True)
    values = ListField(null=True)


db.connect()
db.create_tables([KeyByList])


if __name__ == "__main__":
    if not KeyByList.get_or_none(key="a"):
        KeyByList.create(key="a", values=[1, 2, 3])

    if not KeyByList.get_or_none(key="b"):
        KeyByList.create(key="b", values=None)

    if not KeyByList.get_or_none(key="c"):
        KeyByList.create(key="c", values=[1])

    if not KeyByList.get_or_none(key="e"):
        KeyByList.create(key="e", values=[])

    for x in KeyByList.select():
        print(x.key, x.values)

    # a [1, 2, 3]
    # b None
    # c [1]
    # e []

    print()

    print(KeyByList.get(key="a").values)
    # [1, 2, 3]

    if not KeyByList.get_or_none(key="d"):
        KeyByList.create(key="d", values=list(str(i**2) for i in range(1, 10)))
    print(KeyByList.get(key="d").values)
    # ['1', '4', '9', '16', '25', '36', '49', '64', '81']
