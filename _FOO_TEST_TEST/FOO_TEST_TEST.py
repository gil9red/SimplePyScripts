#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shelve
import functools

from uuid import uuid4
from pathlib import Path
from typing import Any


DIR: Path = Path(__file__).resolve().parent
DB_FILE_NAME: Path = DIR / "db.shelve"


class DB:
    db_name: str = str(DB_FILE_NAME)

    def __init__(self):
        self.db: shelve.Shelf | None = None

    def session(*decorator_args, **decorator_kwargs):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                has_db: bool = self.db is not None
                try:
                    if not has_db:
                        self.db = shelve.open(self.db_name, writeback=True)
                    return func(self, *args, **kwargs)
                finally:
                    if not has_db and self.db is not None:
                        self.db.close()
                        self.db = None

            return wrapped

        return actual_decorator

    @session()
    def get_value(self, name: str, default: Any = None) -> Any:
        if not name:
            return dict(self.db)

        if name not in self.db:
            return default
        return self.db.get(name)

    @session()
    def set_value(self, name: str, value: Any):
        self.db[name] = value

    def inc_value(self, name: str) -> int:
        value = self.get_value(name, default=0)
        value += 1
        self.set_value(name, value)
        return value


db = DB()
print("name", db.get_value("name"))

db.set_value("name", 123)

users: dict[str, dict[str, Any]] = db.get_value("users", default=dict())
print("users", users)
if not users:
    users["Foo"] = dict(name="Foo", age=12)
    users["Bar"] = dict(name="Bar", age=12)
    db.set_value("users", users)

counter: dict[str, int] = db.get_value("counter", default=dict())
print("counter", counter)
if "value" not in counter:
    counter["value"] = 0
counter["value"] += 1
db.set_value("counter", counter)

print([db.inc_value("age") for _ in range(3)])

print(dict(db.get_value("")))
