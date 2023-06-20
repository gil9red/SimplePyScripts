#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import shutil
import sys

from pathlib import Path
from typing import Iterable, Type, TypeVar

# pip install peewee
from peewee import (
    Model,
    SqliteDatabase,
    TextField,
    DateTimeField,
    IntegerField,
    CharField,
    ForeignKeyField,
)

DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent.parent))
from shorten import shorten


# Absolute file name
DB_FILE_NAME = str(DIR / "db.sqlite")
DIR_BACKUP = DIR / "backup"


def db_create_backup(backup_dir=DIR_BACKUP):
    backup_dir.mkdir(parents=True, exist_ok=True)

    file_name = str(DT.datetime.today().date()) + ".sqlite"
    file_name = backup_dir / file_name

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={"foreign_keys": 1})


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


class ProfileRating(BaseModel):
    url = TextField()
    date = DateTimeField(default=DT.datetime.now)
    value = IntegerField()

    @classmethod
    def append(cls, url: str, value: int) -> "ProfileRating":
        return cls.get_or_create(url=url, value=value)[0]


db.connect()
db.create_tables(BaseModel.get_inherited_models())


if __name__ == "__main__":
    BaseModel.print_count_of_tables()
    print()

    print(ProfileRating.get_last())
