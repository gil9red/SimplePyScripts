#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from typing import List, Iterable, Optional

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


class ListField(Field):
    def python_value(self, value: str) -> List:
        return json.loads(value, encoding='utf-8')

    def db_value(self, value: Optional[Iterable]) -> str:
        if value is not None:
            if not isinstance(value, list):
                raise Exception('Type must be a list')

        return json.dumps(value, ensure_ascii=False)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    name = CharField()
    site = CharField()
    genres = ListField()

    @classmethod
    def exists(cls, site: str, name: str) -> bool:
        return cls.select().where(
            cls.site == site, cls.name == name
        ).exists()

    @classmethod
    def add(cls, site: str, name: str, genres: list):
        if not cls.exists(site, name):
            cls.create(site=site, name=name, genres=genres)

    @classmethod
    def get_games_by_site(cls, site: str) -> List['Game']:
        return list(cls.select().where(cls.site == site))

    class Meta:
        indexes = (
            (("name", "site"), True),
        )

    def __repr__(self):
        return f'Game(name={self.name!r}, site={self.site!r}, genres={self.genres})'

    def __str__(self):
        return repr(self)


db.connect()
db.create_tables([Game])


if __name__ == '__main__':
    Game.add(site='foo', name='123', genres=['RPG', 'Action'])
    Game.add(site='foo', name='456', genres=['RPG'])

    for game in Game.select():
        print(game)

    # Game(name='123', site='foo', genres=['RPG', 'Action'])
    # Game(name='456', site='foo', genres=['RPG'])

    print()

    print(Game.get_games_by_site('foo'))
    # [Game(name='123', site='foo', genres=['RPG', 'Action']), Game(name='456', site='foo', genres=['RPG'])]
