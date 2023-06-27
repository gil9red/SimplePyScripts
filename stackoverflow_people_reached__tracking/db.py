#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import os
import pathlib
import re
import shutil

# pip install peewee
from peewee import *


DB_FILE_NAME = str(pathlib.Path(__file__).resolve().parent / "db.sqlite")


def db_create_backup(backup_dir="backup"):
    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(DT.datetime.today().date()) + ".sqlite"
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class PeopleReached(BaseModel):
    url = TextField()
    date = DateTimeField(default=DT.datetime.now)
    value_human = TextField()
    value = IntegerField()

    class Meta:
        indexes = (
            (("url", "value_human"), True),
        )

    @staticmethod
    def append(url: str, value_human: str) -> "PeopleReached":
        match = re.search(r"(\d+\.?\d*)([km])", value_human, flags=re.IGNORECASE)
        if not match:
            raise ValueError(
                f"Invalid value_human ({repr(value_human)}) argument value format!"
            )

        # 750k   -> 750000
        # 112.5m -> 112500000
        units = {
            "k": 1_000,
            "m": 1_000_000,
        }
        value = float(match.group(1))
        unit = match.group(2).lower()
        value = int(value * units[unit])

        return PeopleReached.get_or_create(
            url=url, value_human=value_human, value=value
        )[0]

    def __str__(self):
        return (
            f"PeopleReached(id={self.id}, url={repr(self.url)}, date={self.date}, "
            f"value_human={repr(self.value_human)}, value={self.value})"
        )


db.connect()
db.create_tables([PeopleReached])


if __name__ == "__main__":
    # NOTE: test data
    URL = "https://ru.stackoverflow.com/users/201445/gil9red"
    # PeopleReached.append(URL, '~413k')
    # PeopleReached.append(URL, '~414k')
    # PeopleReached.append(URL, '~415k')
    # PeopleReached.append(URL, '~416k')
    # OR:
    # PeopleReached.get_or_create(url=URL, value_human='~413k', value=413000, date=DT.datetime(2019, 1, 1))
    # PeopleReached.get_or_create(url=URL, value_human='~414k', value=414000, date=DT.datetime(2019, 2, 11))
    # PeopleReached.get_or_create(url=URL, value_human='~415k', value=415000, date=DT.datetime(2019, 3, 15))
    # PeopleReached.get_or_create(url=URL, value_human='~416k', value=416000, date=DT.datetime(2019, 4, 19))

    for x in PeopleReached.select():
        print(x)
