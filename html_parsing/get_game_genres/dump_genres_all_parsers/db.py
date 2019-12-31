#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from typing import List, Iterable, Optional
from pathlib import Path

# pip install peewee
from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase

DB_DIR_NAME = 'database'

# Absolute file name
import pathlib
DB_FILE_NAME = str(pathlib.Path(__file__).resolve().parent / DB_DIR_NAME / 'games.sqlite')

Path(DB_DIR_NAME).mkdir(parents=True, exist_ok=True)


def db_create_backup(backup_dir='backup', date_fmt='%d%m%y'):
    import datetime as DT
    import shutil

    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)

    zip_name = DT.datetime.today().strftime(date_fmt)
    zip_name = backup_path / zip_name

    shutil.make_archive(
        zip_name,
        'zip',
        DB_DIR_NAME
    )


class ListField(Field):
    def python_value(self, value: str) -> List:
        return json.loads(value, encoding='utf-8')

    def db_value(self, value: Optional[Iterable]) -> str:
        if value is not None:
            if not isinstance(value, list):
                raise Exception('Type must be a list')

        return json.dumps(value, ensure_ascii=False)


# Simple Sqlite
# db = SqliteDatabase(
#     DB_FILE_NAME,
#     pragmas={
#         'foreign_keys': 1,        # Ensure foreign-key constraints are enforced.
#         'journal_mode': 'wal',    # WAL-mode
#         'cache_size': -32 * 1000  # 32MB page-cache
#     }
# )
#
# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas=(
        ('foreign_keys', 1),
        ('journal_mode', 'wal'),    # WAL-mode
        ('cache_size', -32 * 1000)  # 32MB page-cache
    ),
    use_gevent=False,    # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,   # Max. # of pending writes that can accumulate.
    results_timeout=5.0  # Max. time to wait for query to be executed.
)


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
    print(Game.select().count())

    # Game.add(site='foo', name='123', genres=['RPG', 'Action'])
    # Game.add(site='foo', name='456', genres=['RPG'])
    #
    # for game in Game.select():
    #     print(game)
    #
    # # Game(name='123', site='foo', genres=['RPG', 'Action'])
    # # Game(name='456', site='foo', genres=['RPG'])
    #
    # print()
    #
    # print(Game.get_games_by_site('foo'))
    # # [Game(name='123', site='foo', genres=['RPG', 'Action']), Game(name='456', site='foo', genres=['RPG'])]
