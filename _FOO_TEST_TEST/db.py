#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import time
import sys

from datetime import date
from typing import Type, Iterable, Optional, Any

# pip install peewee
from peewee import (
    Model,
    TextField,
    ForeignKeyField,
    CharField,
    DateField,
    BlobField,
    IntegerField,
    BooleanField,
)
from playhouse.shortcuts import model_to_dict
from playhouse.sqliteq import SqliteQueueDatabase

from config import DIR, DB_FILE_NAME

sys.path.append(str(DIR.parent.parent.parent))
from shorten import shorten


class NotDefinedParameterException(ValueError):
    def __init__(self, parameter_name: str):
        self.parameter_name = parameter_name
        text = f'Parameter "{self.parameter_name}" must be defined!'

        super().__init__(text)


# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        "foreign_keys": 1,
        "journal_mode": "wal",  # WAL-mode
        "cache_size": -1024 * 64,  # 64MB page-cache
    },
    use_gevent=False,  # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,  # Max. # of pending writes that can accumulate.
    results_timeout=5.0,  # Max. time to wait for query to be executed.
)


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_inherited_models(cls) -> list[Type["BaseModel"]]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def print_count_of_tables(cls):
        items = []
        for sub_cls in cls.get_inherited_models():
            name = sub_cls.__name__
            count = sub_cls.select().count()
            items.append(f"{name}: {count}")

        print(", ".join(items))

    @classmethod
    def count(cls, filters: Iterable = None) -> int:
        query = cls.select()
        if filters:
            query = query.filter(*filters)
        return query.count()

    def to_dict(self) -> dict[str, Any]:
        return model_to_dict(self, recurse=False)

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if isinstance(v, enum.Enum):
                    v = v.value

                if v:
                    v = repr(shorten(v, length=30))

            if isinstance(field, BlobField) and v is not None:
                v = f"<{len(v)} bytes>"

            elif isinstance(field, ForeignKeyField):
                k = f"{k}_id"
                if v:
                    v = v.id

            fields.append(f"{k}={v}")

        return self.__class__.__name__ + "(" + ", ".join(fields) + ")"


class Counter(BaseModel):
    name = CharField(primary_key=True)
    value = IntegerField(default=0)

    @classmethod
    def get_or_create(cls, name: str) -> "Counter":
        obj: Counter | None = cls.get_or_none(name=name)
        if not obj:
            obj = cls.create(name=name)
        return obj

    def inc(self):
        cls = type(self)
        cls.update(value=cls.value + 1).where(cls.name == self.name).execute()


db.connect()
db.create_tables(BaseModel.get_inherited_models())


# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)


if __name__ == "__main__":
    BaseModel.print_count_of_tables()

    counter_foo: Counter = Counter.get_or_create(name="foo")
    counter_foo.inc()
    print(counter_foo)
