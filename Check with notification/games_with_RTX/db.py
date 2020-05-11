#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

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
    name = TextField(unique=True)
    url = TextField(unique=True)
    img_base64 = TextField()
    append_date = DateField(default=DT.date.today)

    def __str__(self):
        return f'Game(id={self.id}, title={self.name!r}, ' \
               f'url={self.url!r}, ' \
               f'img_base64=<{len(self.img_base64)} chars>)'


db.connect()
db.create_tables([Game])


if __name__ == '__main__':
    for game in Game.select():
        print(game)
