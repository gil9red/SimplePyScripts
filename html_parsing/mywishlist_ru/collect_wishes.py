#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import traceback

from datetime import datetime
from pathlib import Path
from typing import Type

# pip install peewee
from peewee import SqliteDatabase, Model, TextField, CharField, DateTimeField

from requests.exceptions import HTTPError

from get_wish_info import Wish as WishInfo
from get_last_id_wish import get_last_id_wish


DIR = Path(__file__).resolve().parent


def get_mandatory_last_id_wish() -> int:
    while True:
        try:
            return get_last_id_wish()
        except Exception:
            print(
                f"Ошибка при получении id последнего желания:\n{traceback.format_exc()}"
            )
            time.sleep(60)


def get_wish_data(wish: WishInfo) -> dict:
    wish_data = wish.as_dict()

    created_at_str = wish_data["created_at"]
    if created_at_str:
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M")
    else:
        created_at = None

    wish_data["created_at"] = created_at

    return wish_data


db = SqliteDatabase(DIR / "dump.sqlite")


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

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                v = repr(v)

            fields.append(f"{k}={v}")

        return self.__class__.__name__ + "(" + ", ".join(fields) + ")"


class Wish(BaseModel):
    user = TextField(null=True)
    user_url = TextField(null=True)
    title = TextField(null=True)
    created_at = DateTimeField(null=True)
    img_url = TextField(null=True)
    error = TextField(null=True)


db.connect()
db.create_tables(BaseModel.get_inherited_models())


def run():
    wish_id = 1
    last_id_wish = get_mandatory_last_id_wish()

    if current_last_id := Wish.select(Wish.id).order_by(Wish.id.desc()).scalar():
        wish_id = current_last_id + 1

    while wish_id < last_id_wish:
        print(f"#{wish_id}")

        try:
            if wish_info := WishInfo.parse_from(wish_id):
                wish_data = get_wish_data(wish_info)
                Wish.create(**wish_data)
            else:
                print(f"#{wish_id} не найдено!")

        except Exception as e:
            error_text = traceback.format_exc()

            # Если ошибка сети, но главная страница доступна
            # Например, у "http://mywishlist.ru/wish/41985" стабильно выдавало 500 ошибку
            if isinstance(e, HTTPError) and get_last_id_wish(safe=True):
                Wish.create(
                    id=wish_id,
                    error=error_text,
                )
            else:
                print(error_text)
                time.sleep(60)
                continue

        wish_id += 1
        time.sleep(0.050)

        # Достигли максимального известного id - попробуем его обновить
        if wish_id == last_id_wish:
            last_id_wish = get_mandatory_last_id_wish()


if __name__ == "__main__":
    run()
