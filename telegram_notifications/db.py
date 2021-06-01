#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import sys

import enum
from typing import List, Any

# pip install peewee
from peewee import (
    Model, TextField, ForeignKeyField, DateTimeField, CharField, IntegerField
)
from playhouse.sqliteq import SqliteQueueDatabase

from telegram_notifications.config import DIR
from telegram_notifications.common import TypeEnum

# Для импортирования shorten
sys.path.append(str(DIR.parent))
from shorten import shorten


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


class EnumField(CharField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, choices: enum.Enum, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.choices: enum.Enum = choices
        self.max_length = 255

    def db_value(self, value: Any) -> Any:
        return value.value

    def python_value(self, value: Any) -> Any:
        type_value_enum = type(list(self.choices)[0].value)
        value_enum = type_value_enum(value)
        return self.choices(value_enum)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if v:
                    if isinstance(v, enum.Enum):
                        v = v.value

                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f'{k}_id'
                if v:
                    v = v.id

            fields.append(f'{k}={v}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'


class Notification(BaseModel):
    chat_id = IntegerField()
    name = TextField()
    message = TextField()
    type = EnumField(null=False, choices=TypeEnum, default=TypeEnum.INFO)
    append_datetime = DateTimeField(default=DT.datetime.now)
    sending_datetime = DateTimeField(null=True)

    @classmethod
    def add(cls, chat_id: int, name: str, message: str, type=TypeEnum.INFO) -> 'Notification':
        return cls.create(
            chat_id=chat_id,
            name=name,
            message=message,
            type=type,
        )

    @classmethod
    def get_unsent(cls) -> List['Notification']:
        """
        Функция класс, что возвращает неотправленные уведомления
        """

        return list(cls.select().where(cls.sending_datetime.is_null(True)))

    def set_as_send(self):
        """
        Функция устанавливает дату отправки и сохраняет ее
        """

        self.sending_datetime = DT.datetime.now()
        self.save()

    def get_html(self) -> str:
        """
        Функция возвращает текст для отправки запроса в формате HTML
        """

        return f'{self.type.emoji} <b>{self.name}</b>\n{self.message}'


db.connect()
db.create_tables([Notification])


if __name__ == '__main__':
    # Notification.delete().execute()

    # Notification.add(
    #     chat_id=1,
    #     name='check',
    #     message='ALL OK!',
    #     type=TypeEnum.INFO,
    # )

    for x in Notification.select():
        print(x)
    #     print(x.get_html())

    print('Unsent:', len(Notification.get_unsent()))

    # print()
    #
    # for x in Notification.get_unsent():
    #     print(x)
    #     x.set_as_send()
