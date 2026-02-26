#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/coleifer/peewee/blob/afdf7b752dcadbf440faaa91a7fb0f403eac9a69/examples/diary.py


import datetime as dt

from textwrap import shorten

# pip install peewee
from peewee import Model, SqliteDatabase, TextField, DateTimeField


db = SqliteDatabase("my_database.sqlite")


class BaseModel(Model):
    class Meta:
        database = db


class Diary(BaseModel):
    content = TextField()
    created_date = DateTimeField(default=dt.datetime.now)

    @staticmethod
    def print_table(search_text: str = None) -> None:
        """Print all diaries"""

        header_fmt = "{:<3}  | {:<50} | {:<19}"
        row_fmt = "#{id:<3} | {content:<50} | {created_date:%d/%m/%Y %H:%M:%S}"

        print(header_fmt.format(*map(str.upper, Diary._meta.fields)))

        query = Diary.select()
        if search_text:
            query = query.where(Diary.content.contains(search_text))

        for diary in query:
            print(
                row_fmt.format(
                    id=diary.id,
                    content=shorten(diary.content, width=50, placeholder="..."),
                    created_date=diary.created_date,
                )
            )

        print()

    def __str__(self) -> str:
        return (
            f"Diary<"
            f"#{self.id} "
            f'content={repr(shorten(self.content, width=50, placeholder="..."))} '
            f"created_date='{self.created_date:%d/%m/%Y %H:%M:%S}'"
            f">"
        )


db.connect()
db.create_tables([Diary])


# Вызываем в первый раз, чтобы заполнить таблицу
if not Diary.select().count():
    Diary.create(content="Hello World!")
    Diary.create(content="The quick brown fox jumps over the lazy dog.")


def add_diary() -> None:
    """Add diary"""

    data = input("Enter your diary: ").strip()
    if data and input("Save diary? [Y/n] ") != "n":
        Diary.create(content=data)
        print("Saved successfully.")


def view_diaries(search_query=None) -> None:
    """View previous diaries"""

    query = Diary.select().order_by(Diary.created_date.desc())
    if search_query:
        query = query.where(Diary.content.contains(search_query))

    for diary in query:
        print()
        timestamp = diary.created_date.strftime("%d/%m/%Y %H:%M:%S")
        print(timestamp)
        print("=" * len(timestamp))
        print(diary.content)
        print()
        print("n) next diary")
        print("d) delete diary")
        print("q) return to main menu")
        action = input("Choice? (N/d/q) ").lower().strip()
        if action == "q":
            break
        elif action == "d":
            diary.delete_instance()
            break


def search_diaries() -> None:
    """Search diaries"""

    view_diaries(input("Search query: "))


MENU = dict(
    [
        ("a", add_diary),
        ("v", view_diaries),
        ("s", search_diaries),
        ("p", Diary.print_table),
    ]
)


def menu_loop() -> None:
    choice = None
    while choice != "q":
        for key, value in MENU.items():
            print("%s) %s" % (key, value.__doc__))
        choice = input("Action: ").lower().strip()
        if choice in MENU:
            MENU[choice]()


Diary.print_table()

menu_loop()
