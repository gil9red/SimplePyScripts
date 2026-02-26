#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil
import sys
import time

from datetime import datetime
from typing import Optional, Type
from pathlib import Path

# pip install peewee
from peewee import TextField, DateTimeField, ForeignKeyField, IntegerField, BooleanField, Model
from playhouse.sqliteq import SqliteQueueDatabase

# pip install python-telegram-bot
import telegram

sys.path.append("../../")
from shorten import shorten


DIR = Path(__file__).resolve().parent
DB_DIR_NAME = DIR / "database"
DB_FILE_NAME = str(DB_DIR_NAME / "database.sqlite")

DB_DIR_NAME.mkdir(parents=True, exist_ok=True)


def db_create_backup(backup_dir="backup", date_fmt="%Y-%m-%d") -> None:
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)

    zip_name = datetime.today().strftime(date_fmt)
    zip_name = backup_path / zip_name

    shutil.make_archive(zip_name, "zip", DB_DIR_NAME)


# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        "foreign_keys": 1,
        "journal_mode": "wal",  # WAL-mode
        "cache_size": -1024 * 64,  # 64MB page-cache
    },
    use_gevent=False,  # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,  # Max. # of pending writes that can accumulate.
    results_timeout=5.0,  # Max. time to wait for query to be executed.
)


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_inherited_models(cls) -> list[Type["BaseModel"]]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def print_count_of_tables(cls) -> None:
        items = []
        for sub_cls in cls.get_inherited_models():
            name = sub_cls.__name__
            count = sub_cls.select().count()
            items.append(f"{name}: {count}")

        print(", ".join(items))

    def __str__(self) -> str:
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, TextField):
                if v:
                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f"{k}_id"
                if v:
                    v = v.id

            fields.append(f"{k}={v}")

        return self.__class__.__name__ + "(" + ", ".join(fields) + ")"


# SOURCE: https://core.telegram.org/bots/api#user
class User(BaseModel):
    first_name = TextField()
    last_name = TextField(null=True)
    username = TextField(null=True)
    language_code = TextField(null=True)
    last_activity = DateTimeField(default=datetime.now)

    def update_last_activity(self) -> None:
        self.last_activity = datetime.now()
        self.save()

    @classmethod
    def get_from(cls, user: Optional[telegram.User]) -> Optional["User"]:
        if not user:
            return

        user_db = cls.get_or_none(cls.id == user.id)
        if not user_db:
            user_db = cls.create(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                language_code=user.language_code,
            )
        return user_db


# SOURCE: https://core.telegram.org/bots/api#chat
class Chat(BaseModel):
    type = TextField()
    title = TextField(null=True)
    username = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    description = TextField(null=True)
    last_activity = DateTimeField(default=datetime.now)

    def update_last_activity(self) -> None:
        self.last_activity = datetime.now()
        self.save()

    @classmethod
    def get_from(cls, chat: Optional[telegram.Chat]) -> Optional["Chat"]:
        if not chat:
            return

        chat_db = cls.get_or_none(cls.id == chat.id)
        if not chat_db:
            chat_db = cls.create(
                id=chat.id,
                type=chat.type,
                title=chat.title,
                username=chat.username,
                first_name=chat.first_name,
                last_name=chat.last_name,
                description=chat.description,
            )
        return chat_db


class Reminder(BaseModel):
    date_time = DateTimeField(default=datetime.now)
    message_id = IntegerField()
    command = TextField()
    finish_time = DateTimeField(default=datetime.now)
    is_sent = BooleanField(default=False)
    user = ForeignKeyField(User, backref="reminders")
    chat = ForeignKeyField(Chat, backref="reminders")


db.connect()
db.create_tables(BaseModel.get_inherited_models())

# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)


if __name__ == "__main__":
    BaseModel.print_count_of_tables()
    print()

    print("Total users:", User.select().count())
    print("Total chats:", Chat.select().count())

    assert User.get_from(None) is None
    assert Chat.get_from(None) is None

    print()

    first_user = User.select().first()
    print("First user:", first_user)

    first_chat = Chat.select().first()
    print("First chat:", first_chat)
    print()

    print("Total reminders:", Reminder.select().count())
    print()

    print("Last reminder:", Reminder.select().order_by(Reminder.id.desc()).first())
