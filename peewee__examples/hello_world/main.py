#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install peewee
from peewee import Model, SqliteDatabase, TextField, IntegerField


db = SqliteDatabase("my_database.sqlite")


class Info(Model):
    first_name = TextField()
    second_name = TextField()
    state = IntegerField()

    class Meta:
        database = db

    def __str__(self) -> str:
        return f"Info<#{self.id} first_name={self.first_name!r} second_name={self.second_name!r} state={self.state}>"


db.connect()
db.create_tables([Info])


if __name__ == "__main__":
    # Вызываем в первый раз, чтобы заполнить таблицу
    if not Info.select().count():
        for i in range(5):
            Info.create(
                first_name="first_name_" + str(i),
                second_name="second_name_" + str(i),
                state=i,
            )

    for info in Info.select():
        print(info)
    """
    Info<#1 first_name='Четный state!' second_name='second_name_0' state=0>
    Info<#2 first_name='first_name_1' second_name='second_name_1' state=1>
    Info<#3 first_name='Четный state!' second_name='second_name_2' state=2>
    Info<#4 first_name='first_name_3' second_name='second_name_3' state=3>
    Info<#5 first_name='Четный state!' second_name='second_name_4' state=4>
    """

    for info in Info.select():
        if info.state % 2 == 0:
            info.first_name = "Четный state!"
            info.save()

    print()

    for info in Info.select():
        print(info)
    """
    Info<#1 first_name='Четный state!' second_name='second_name_0' state=0>
    Info<#2 first_name='first_name_1' second_name='second_name_1' state=1>
    Info<#3 first_name='Четный state!' second_name='second_name_2' state=2>
    Info<#4 first_name='first_name_3' second_name='second_name_3' state=3>
    Info<#5 first_name='Четный state!' second_name='second_name_4' state=4>
    """
