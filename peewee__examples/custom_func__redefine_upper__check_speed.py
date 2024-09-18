#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: Analog https://github.com/gil9red/SimplePyScripts/blob/7b0238202c6e6b5750ff6909d0a78b7892ee1767/sqlite3__examples/custom_func__redefine_upper__check_speed.py


import random

from timeit import default_timer, timeit
from typing import Type, Iterable, Self, Any

# pip install peewee
from peewee import (
    SqliteDatabase,
    Model,
    TextField,
    DecimalField,
    fn
)
from playhouse.shortcuts import model_to_dict


db = SqliteDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_inherited_models(cls) -> list[Type[Self]]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def count(cls, filters: Iterable = None) -> int:
        query = cls.select()
        if filters:
            query = query.filter(*filters)
        return query.count()

    def to_dict(self) -> dict[str, Any]:
        return model_to_dict(self, recurse=False)


class Stocks(BaseModel):
    date = TextField()
    trans = TextField()
    symbol = TextField()
    qty = DecimalField()
    price = DecimalField()


db.connect()
db.create_tables(BaseModel.get_inherited_models())

print("Generate items...")
t = default_timer()
purchases = [
    Stocks(
        date=random.choice(["2006-03-28", "2006-04-05", "2006-04-06"]),
        trans=random.choice(["SELL", "BUY"]),
        symbol=random.choice(["IBM", "MSFT"]),
        qty=random.choice([500, 1000, 600]),
        price=random.choice([53.00, 45.00, 72.00]),
    )
    for _ in range(500_000)
]
print(f"Elapsed {default_timer() - t:.3f} secs")
# Elapsed 2.097 secs

print()

print("INSERT INTO...")
t = default_timer()

with db.atomic():
    Stocks.bulk_create(purchases, batch_size=5_000)

print(f"Elapsed {default_timer() - t:.3f} secs")
# Elapsed 6.842 secs

print()


def run_test():
    elapsed = timeit(
        stmt="Stocks.select().where(fn.UPPER(Stocks.trans).ilike(fn.UPPER('%SELL%'))).count()",
        globals=dict(Stocks=Stocks, fn=fn),
        number=100,
    )
    print(f"Elapsed {elapsed:.3f} secs")


print("SELECT COUNT DEFAULT UPPER...")
run_test()
# Elapsed 11.765 secs

print()


@db.func("upper")
def upper(value: str) -> str | None:
    if value is None:
        return
    return value.upper()


print("SELECT COUNT PYTHON UPPER...")
run_test()
# Elapsed 47.276 secs
