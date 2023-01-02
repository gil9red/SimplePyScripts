#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
import shutil

from collections import defaultdict
from typing import Iterable, Optional, Type
from pathlib import Path

# pip install peewee
from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase

from shorten import shorten


DIR = Path(__file__).resolve().parent

DB_DIR_NAME = DIR / 'database'
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

DB_FILE_NAME = str(DB_DIR_NAME / 'games.sqlite')


def db_create_backup(backup_dir=DIR / 'backup', date_fmt='%Y-%m-%d'):
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
    field_type = 'TEXT'

    def python_value(self, value: str) -> list:
        return json.loads(value)

    def db_value(self, value: Optional[Iterable]) -> str:
        if value is not None:
            if isinstance(value, str):
                return value

            if not isinstance(value, list):
                raise Exception('Type must be a list')

        return json.dumps(value, ensure_ascii=False)


# Simple Sqlite
# db = SqliteDatabase(
#     DB_FILE_NAME,
#     pragmas={
#         'foreign_keys': 1,        # Ensure foreign-key constraints are enforced.
#         'journal_mode': 'wal',    # WAL-mode
#         'cache_size': -1024 * 64  # 64MB page-cache
#     }
# )
#
# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        'foreign_keys': 1,
        'journal_mode': 'wal',    # WAL-mode
        'cache_size': -1024 * 64  # 64MB page-cache
    },
    use_gevent=False,    # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,   # Max. # of pending writes that can accumulate.
    results_timeout=5.0  # Max. time to wait for query to be executed.
)


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_inherited_models(cls) -> list[Type['BaseModel']]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def print_count_of_tables(cls):
        items = []
        for sub_cls in cls.get_inherited_models():
            name = sub_cls.__name__
            count = sub_cls.select().count()
            items.append(f'{name}: {count}')

        print(', '.join(items))

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
                k = f'{k}_id'
                if v:
                    v = v.id

            fields.append(f'{k}={v}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'


class Dump(BaseModel):
    name = CharField()
    site = CharField()
    genres = ListField()

    class Meta:
        indexes = (
            (("name", "site"), True),
        )

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
    def get(cls) -> list['Dump']:
        return cls.select().where(cls.genres != '[]').order_by(cls.name)

    @classmethod
    def get_games_by_site(cls, site: str) -> list['Dump']:
        return list(cls.select().where(cls.site == site).order_by(cls.name))

    @classmethod
    def get_genres_by_game(cls, game_name: str) -> list[str]:
        items = []

        for dump in cls.select().where(cls.name == game_name):
            items += dump.genres

        return sorted(set(items))

    @classmethod
    def get_all_genres(cls) -> list[str]:
        items = []

        for dump in cls.select():
            items += dump.genres

        return sorted(set(items))

    @classmethod
    def get_all_games(cls) -> list[str]:
        return [
            dump.name
            for dump in cls.select(cls.name).order_by(cls.name).distinct()
        ]

    @classmethod
    def get_all_sites(cls) -> list[str]:
        return [
            dump.site
            for dump in cls.select(cls.site).order_by(cls.site).distinct()
        ]

    @classmethod
    def dump(cls) -> dict[str, list[str]]:
        game_by_genres = defaultdict(list)

        for dump in cls.select().order_by(cls.name):
            game_by_genres[dump.name] += dump.genres

        for k, v in game_by_genres.items():
            game_by_genres[k] = sorted(set(v))

        return game_by_genres

    def __repr__(self):
        return f'Dump(name={self.name!r}, site={self.site!r}, genres={self.genres})'

    def __str__(self):
        return repr(self)


db.connect()
db.create_tables(BaseModel.get_inherited_models())


if __name__ == '__main__':
    BaseModel.print_count_of_tables()
    print()

    print('Total:', Dump.select().count())

    genres = Dump.get_all_genres()
    print(f'Genres ({len(genres)}): {genres}')

    games = Dump.get_all_games()
    print(f'Games ({len(games)}): {games}')

    sites = Dump.get_all_sites()
    print(f'Sites ({len(sites)}): {sites}')

    print()

    print(Dump.get_genres_by_game('Dead Space'))
    # ['3D', 'Action', 'Adventure: Survival Horror', 'Arcade', 'Sci-Fi', 'Shooter', 'Third-Person', 'action',
    # 'Боевик', 'Боевик от третьего лица', 'Боевик-приключения', 'Космос', 'От третьего лица', 'Ужасы', 'Шутер',
    # 'Шутеры', 'Экшен', 'Экшены', 'ужасы']

    # print()
    #
    # for x in Dump.get():
    #     print(x)
    #
    # print()

    #
    # For testing
    #
    # Dump.add(site='foo', name='123', genres=['RPG', 'Action'])
    # Dump.add(site='foo', name='456', genres=['RPG'])
    #
    # for dump in Dump.select():
    #     print(dump)
    #
    # # Dump(name='123', site='foo', genres=['RPG', 'Action'])
    # # Dump(name='456', site='foo', genres=['RPG'])
    #
    # print()
    #
    # print(Dump.get_games_by_site('foo'))
    # # [Dump(name='123', site='foo', genres=['RPG', 'Action']), Dump(name='456', site='foo', genres=['RPG'])]
