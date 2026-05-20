#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum

# pip install peewee
from peewee import SqliteDatabase, Model

from db_enum_field import EnumField


@enum.unique
class TaskRunStatusEnum(enum.StrEnum):
    PENDING = enum.auto()
    RUNNING = enum.auto()
    FINISHED = enum.auto()
    STOPPED = enum.auto()
    UNKNOWN = enum.auto()
    ERROR = enum.auto()


db = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class TaskRun(BaseModel):
    status = EnumField(choices=TaskRunStatusEnum, default=TaskRunStatusEnum.PENDING)


db.connect()
db.create_tables([TaskRun])


if __name__ == "__main__":
    run1 = TaskRun.create()
    run2 = TaskRun.create(status=TaskRunStatusEnum.FINISHED)

    query = TaskRun.select().where(TaskRun.status == TaskRunStatusEnum.FINISHED)
    print(query)
    print(list(query))
    # SELECT "t1"."id", "t1"."status" FROM "taskrun" AS "t1" WHERE ("t1"."status" = 'finished')
    # [<TaskRun: 2>]

    print()

    query = TaskRun.select().where(TaskRun.status.contains("ING"))
    print(query)
    print(list(query))
    # SELECT "t1"."id", "t1"."status" FROM "taskrun" AS "t1" WHERE ("t1"."status" LIKE '%ING%')
    # [<TaskRun: 1>]
