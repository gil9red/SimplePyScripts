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
    BooleanField,
)
from playhouse.shortcuts import model_to_dict
from playhouse.sqliteq import SqliteQueueDatabase

from config import DIR, DB_FILE_NAME

sys.path.append(str(DIR.parent.parent.parent))
from shorten import shorten


class NotDefinedParameterException(ValueError):
    def __init__(self, parameter_name: str) -> None:
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
    def print_count_of_tables(cls) -> None:
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

    def __str__(self) -> str:
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


class Person(BaseModel):
    name = TextField()
    position = TextField()
    department = TextField()
    img = BlobField(default=True)
    location = TextField()
    birthday = TextField()
    create_date = DateField(default=date.today)
    last_check_date = DateField(default=date.today)
    is_active = BooleanField(default=None, null=True)
    prev_name = TextField(default=None, null=True)

    class Meta:
        indexes = (
            # Уникальный индекс по name и дате создания
            (("name", "create_date"), True),
        )

    @classmethod
    def get_last_by_name(cls, name: str) -> Optional["Person"]:
        items: list[Person] = cls.get_all(name)
        return items[0] if items else None

    @classmethod
    def get_all(cls, name: str) -> list["Person"]:
        prev_names: set[str] = set()

        persons: set[Person] = set()
        for p in cls.select().where(cls.name == name):
            persons.add(p)

            if p.prev_name:
                prev_names.add(p.prev_name)

        for prev_name in prev_names:
            if prev_name in persons:
                continue

            for p in Person.get_all(prev_name):
                persons.add(p)

        return sorted(persons, key=lambda p: p.id, reverse=True)

    @classmethod
    def get_all_name(cls) -> list[str]:
        return [p.name for p in cls.select(cls.name).distinct()]


db.connect()
db.create_tables(BaseModel.get_inherited_models())


# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)


if __name__ == "__main__":
    BaseModel.print_count_of_tables()
    print()

    names: list[str] = Person.get_all_name()
    persons: list[Person] = [
        Person.get_last_by_name(name)
        for name in names
    ]
    print(f"Total: {len(persons)}")
    print(f"Active: {len([p for p in persons if p.is_active])}")
    print(f"Non active: {len([p for p in persons if not p.is_active])}")

    # Поиск людей с одинаковой картинкой в профиле
    # from collections import defaultdict
    # img_by_persons: defaultdict[bytes, set[str]] = defaultdict(set)
    #
    # for p in Person:
    #     img_by_persons[p.img].add(p.name)
    #
    # for img, persons in sorted(img_by_persons.items(), key=lambda x: len(x[1]), reverse=True):
    #     if len(persons) > 1:
    #         print(len(persons), persons)
    #
