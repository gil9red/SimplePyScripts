#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import sys
import time

from typing import Optional, List

# pip install peewee
from peewee import (
    Model, TextField, ForeignKeyField, CharField
)
from playhouse.sqliteq import SqliteQueueDatabase

from word_to_emoji.config import DIR

# Для импортирования shorten
sys.path.append(str(DIR.parent))
from shorten import shorten

from pymorphy2__examples.normal_form import get_normal_form


DB_DIR_NAME = DIR / 'database'
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

DB_FILE_NAME = str(DB_DIR_NAME / 'database.sqlite')


# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        'foreign_keys': 1,
        'journal_mode': 'wal',    # WAL-mode
        'cache_size': -1024 * 64  # 64MB page-cache
    },
    use_gevent=False,     # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,    # Max. # of pending writes that can accumulate.
    results_timeout=5.0   # Max. time to wait for query to be executed.
)


def preprocess_emoji(emoji: str) -> str:
    if not emoji:
        return emoji

    return re.sub(r'\s{2,}', '', emoji.strip())


class BaseModel(Model):
    class Meta:
        database = db

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


class Word2Emoji(BaseModel):
    word = TextField(unique=True)
    emoji = TextField(null=True)

    @classmethod
    def add(cls, word: str, emoji: str = None):
        word = word.strip()
        word = get_normal_form(word)
        obj = cls.get_or_none(cls.word == word)
        if obj:
            emoji = preprocess_emoji(emoji)
            if emoji:
                obj.emoji = emoji
                obj.save()

        else:
            cls.create(word=word, emoji=emoji)

    @classmethod
    def get_emoji(cls, word: str) -> Optional[str]:
        word = word.strip()
        word = get_normal_form(word)
        val = cls.select().where(cls.word == word).first()
        if val:
            return val.emoji

    @classmethod
    def get_unprocessed_words(cls) -> List[str]:
        return [x.word for x in cls.select().where(cls.emoji.is_null(True))]


db.connect()
db.create_tables([Word2Emoji])

# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)

if __name__ == '__main__':
    Word2Emoji.add('любовь', '💏')
    print(Word2Emoji.get_emoji('любовь'))

    Word2Emoji.add('любовь')
    print(Word2Emoji.get_emoji('любовь'))

    print()

    items = Word2Emoji.get_unprocessed_words()
    print(f'Unprocessed words ({len(items)}): [{", ".join(map(repr, items[:10]))}, ...]')

    print()

    for x in Word2Emoji.select().limit(5):
        print(x)
