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
    KEY_USERS: str = "users"
    KEY_PRODUCTS: str = "products"
    KEY_SHOPPING_CARTS: str = "shopping_carts"

    db_name: str = str(DB_FILE_NAME)
    # db: shelve.Shelf | None = None

    def __init__(self):
        self.db: shelve.Shelf | None = None

    def session(*decorator_args, **decorator_kwargs):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                has_db: bool = self.db is not None
                print("[wrapped]", has_db, self.db)
                try:
                    if not has_db:
                        print("[wrapped] open")
                        self.db = shelve.open(self.db_name, writeback=True)
                    return func(self, *args, **kwargs)
                finally:
                    print("[wrapped] close", has_db, self.db)
                    if not has_db and self.db is not None:
                        print("[wrapped] closed")
                        self.db.close()
                        self.db = None

            return wrapped

        return actual_decorator

    def _generate_id(self) -> str:
        return str(uuid4())

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

print(dict(db.get_value("")))
