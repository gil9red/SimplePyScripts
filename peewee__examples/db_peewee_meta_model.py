#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from enum import Enum
from typing import Type, Any, Iterable

from peewee import CharField, TextField, ForeignKeyField, Model
from playhouse.shortcuts import model_to_dict


def shorten(text: str, length: int = 30, placeholder: str = "...") -> str:
    if not text:
        return text

    if len(text) > length:
        text = text[: length - len(placeholder)] + placeholder
    return text


class MetaModel(Model):
    def get_new(self) -> "MetaModel":
        return type(self).get(self._pk_expr())

    @classmethod
    def get_first(cls) -> "MetaModel":
        return cls.select().first()

    @classmethod
    def get_last(cls) -> "MetaModel":
        return cls.select().order_by(cls.id.desc()).first()

    @classmethod
    def get_inherited_models(cls) -> list[Type["MetaModel"]]:
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
                if isinstance(v, Enum):
                    v = v.value

                if v:
                    v = repr(shorten(v, length=30))

            elif isinstance(field, ForeignKeyField):
                k = f"{k}_id"
                if v:
                    v = v.id

            fields.append(f"{k}={v}")

        return self.__class__.__name__ + "(" + ", ".join(fields) + ")"


if __name__ == "__main__":
    from peewee import SqliteDatabase

    db = SqliteDatabase(":memory:")

    class BaseModel(MetaModel):
        class Meta:
            database = db

    class Data(BaseModel):
        name = CharField()
        value = TextField()

    db.connect()
    db.create_tables(BaseModel.get_inherited_models())

    BaseModel.print_count_of_tables()
    # Data: 0

    data = dict(
        a="aAA",
        b="Foo",
        bar="!!!",
    )
    for k, v in data.items():
        Data.create(name=k, value=v)

    BaseModel.print_count_of_tables()
    # Data: 3

    print()

    print(Data.get_first())
    print(Data.get_last())
    # Data(id=1, name='a', value='aAA')
    # Data(id=3, name='bar', value='!!!')

    print()

    print(Data.get_last().to_dict())
    # {'id': 3, 'name': 'bar', 'value': '!!!'}
