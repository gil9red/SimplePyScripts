#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install peewee
from peewee import *

# Absolute file name
import pathlib
DB_FILE_NAME = str(pathlib.Path(__file__).resolve().parent / 'games.sqlite')


def db_create_backup(backup_dir='backup'):
    import datetime as DT
    import os
    import shutil

    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(DT.datetime.today().date()) + '.sqlite'
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    name = CharField()
    site = CharField()
    genres = TextField()

    class Meta:
        indexes = (
            (("name", "site"), True),
        )

    def __str__(self):
        return f'Game(name={self.name!r}, ' \
               f'site={self.site!r}, ' \
               f'genres={self.genres})'

db.connect()
db.create_tables([Game])


if __name__ == '__main__':
    for game in Game.select():
        print(game)
