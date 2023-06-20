#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from typing import Type, Optional, Iterable, TypeVar
from uuid import uuid4

# pip install peewee
from peewee import Model, TextField, ForeignKeyField, CharField
from playhouse.sqliteq import SqliteQueueDatabase

from config import DB_FILE_NAME, LENGTH_URL_ID
from shorten import shorten


def generate_link_id(length: int = LENGTH_URL_ID) -> str:
    # TODO: Возможна ситуация, когда length будет больше размера UUID
    return uuid4().hex[:length]


class NotDefinedParameterException(Exception):
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
        "journal_mode": "wal",     # WAL-mode
        "cache_size": -1024 * 64,  # 64MB page-cache
    },
    use_gevent=False,     # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,    # Max. # of pending writes that can accumulate.
    results_timeout=5.0,  # Max. time to wait for query to be executed.
)


ChildModel = TypeVar("ChildModel", bound="BaseModel")


class BaseModel(Model):
    """
    Базовая модель классов-таблиц
    """

    class Meta:
        database = db

    def get_new(self) -> ChildModel:
        return type(self).get(self._pk_expr())

    @classmethod
    def get_first(cls) -> ChildModel:
        return cls.select().first()

    @classmethod
    def get_last(cls) -> ChildModel:
        return cls.select().order_by(cls.id.desc()).first()

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

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if v:
                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f"{k}_id"
                if v:
                    v = v.id

            fields.append(f"{k}={v}")

        return self.__class__.__name__ + "(" + ", ".join(fields) + ")"


class Link(BaseModel):
    link_id = TextField(primary_key=True)
    link_url = TextField(unique=True)

    @classmethod
    def get_by_link_url(cls, link_url: str) -> Optional["Link"]:
        if not link_url or not link_url.strip():
            raise NotDefinedParameterException(parameter_name="link_url")

        return cls.get_or_none(cls.link_url == link_url)

    @classmethod
    def get_by_link_id(cls, link_id: str) -> Optional["Link"]:
        if not link_id or not link_id.strip():
            raise NotDefinedParameterException(parameter_name="link_id")

        return cls.get_or_none(cls.link_id == link_id)

    @classmethod
    def add(cls, link_url: str) -> "Link":
        obj = cls.get_by_link_url(link_url)
        if not obj:
            # Убеждаемся, что link_id будет уникальным
            while True:  # TODO: Возможна ситуация, когда свободные закончатся
                link_id = generate_link_id()
                if not cls.get_by_link_id(link_id):
                    break

            obj = cls.create(
                link_id=link_id,
                link_url=link_url,
            )

        return obj


db.connect()
db.create_tables(BaseModel.get_inherited_models())

# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)

if __name__ == "__main__":
    BaseModel.print_count_of_tables()
    # Link: 1
    print()

    link = Link.add(link_url="https://example.com")
    assert Link.select().count()
    assert link == link.get_by_link_url(link_url=link.link_url)
    assert link == link.get_by_link_id(link_id=link.link_id)
