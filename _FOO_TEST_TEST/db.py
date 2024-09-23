#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime
from dataclasses import dataclass, fields
from typing import Any, Generator, Optional, Type

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from config import PATH_DB


def get_fields(class_or_instance) -> list[str]:
    return [f.name for f in fields(class_or_instance)]


db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(str(PATH_DB))
if not db.open():
    raise Exception(db.lastError().text())


class BaseModel:
    @classmethod
    def get_table_name(cls) -> str:
        return cls.__name__

    @classmethod
    def create_table(cls):
        raise NotImplemented()

    @classmethod
    def select(cls, where: dict[str, Any] = None) -> Generator[Type["BaseModel"], None, None]:
        this_fields: list[str] = get_fields(cls)

        if where:
            where_filter = "AND".join(f"{k} = :{k}" for k, v in where.items())
            where_str = f"WHERE {where_filter}"
        else:
            where_str = ""

        query = QSqlQuery()
        query.prepare(
            f"""
            SELECT {",".join(this_fields)}
            FROM {cls.get_table_name()}
            {where_str}
            """
        )
        if where:
            for k, v in where.items():
                query.bindValue(f":{k}", v)
        query.exec()

        while query.next():
            data: dict[str, Any] = {
                name: query.value(name)
                for name in this_fields
            }
            yield cls(**data)

    @classmethod
    def select_one(cls, where: dict[str, Any] = None) -> Optional[Type["BaseModel"]]:
        return next(
            cls.select(where=where),
            None,
        )

    @classmethod
    def get_inherited_models(cls) -> list[Type["BaseModel"]]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)


@dataclass
class Logged(BaseModel):
    id: int
    date: str
    total_seconds: int
    total_seconds_human: str

    @classmethod
    def create_table(cls):
        QSqlQuery(
            f"""
            CREATE TABLE IF NOT EXISTS {cls.get_table_name()}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date VARCHAR(10) UNIQUE,
                total_seconds INTEGER DEFAULT 0,
                total_seconds_human TEXT
            )
            """
        ).exec()

    @classmethod
    def get_by_date(cls, date: str) -> Optional["Logged"]:
        return cls.select_one(where=dict(date=date))

    @classmethod
    def add(cls, date: str) -> "Logged":
        # Если уже есть
        if obj := cls.get_by_date(date):
            return obj

        query = QSqlQuery()
        query.prepare(f"INSERT INTO {cls.get_table_name()} (date) VALUES (:date)")
        query.bindValue(":date", date)
        query.exec()

        return cls.get_by_date(date)


@dataclass
class LoggedItem(BaseModel):
    uuid: str
    logged_id: int
    time: str
    seconds: int
    seconds_human: str
    jira_id: str
    jira_title: str

    @classmethod
    def create_table(cls):
        QSqlQuery(
            f"""
            CREATE TABLE IF NOT EXISTS {cls.get_table_name()}(
                uuid TEXT PRIMARY KEY,
                logged_id INTEGER,
                time VARCHAR(8),
                seconds INTEGER DEFAULT 0,
                seconds_human TEXT,
                jira_id TEXT,
                jira_title TEXT,
                
                FOREIGN KEY (logged_id) REFERENCES Logged (id) ON DELETE CASCADE
            )
            """
        ).exec()

    @classmethod
    def get_by_uuid(cls, uuid: str) -> Optional["LoggedItem"]:
        return cls.select_one(where=dict(uuid=uuid))

    @classmethod
    def add(
        cls,
        uuid: str,
        date_time: datetime,
        seconds: int,
        seconds_human: str,
        jira_id: str,
        jira_title: str,
    ) -> "LoggedItem":
        # Если уже есть
        if obj := cls.get_by_uuid(uuid):
            return obj

        date_str = date_time.date().isoformat()
        logged_id = Logged.add(date_str).id

        query = QSqlQuery()
        query.prepare(
            f"""
            INSERT INTO {cls.get_table_name()} (uuid, logged_id, time, seconds, seconds_human, jira_id, jira_title)
            VALUES (:uuid, :logged_id, :time, :seconds, :seconds_human, :jira_id, :jira_title)
            """
        )
        query.bindValue(":uuid", uuid)
        query.bindValue(":logged_id", logged_id)
        query.bindValue(":time", date_time.time().isoformat())
        query.bindValue(":seconds", seconds)
        query.bindValue(":seconds_human", seconds_human)
        query.bindValue(":jira_id", jira_id)
        query.bindValue(":jira_title", jira_title)
        query.exec()

        return cls.get_by_uuid(uuid)


for model in BaseModel.get_inherited_models():
    model.create_table()


# date = "2024-09-23"
# print(Logged.get_by_date(date))
# print(Logged.add(date))
# print(Logged.add(date))
# print(Logged.get_by_date(date))
# print()
#
# for obj in Logged.select():
#     print(obj)

items = [
    {
        "uuid": "bf5540c1-2614-4521-898c-64fcd2222c1d",
        "date_time": "24/08/2024 21:46:41",
        "date": "24/08/2024",
        "time": "21:46:41",
        "logged_human_time": "1 hour",
        "logged_seconds": 3600,
        "jira_id": "FOO-11202",
        "jira_title": "Учет времени, не связанного с конкретной джирой"
    },
    {
        "uuid": "e8ea6140-daa2-46ca-981f-bee449fe4a34",
        "date_time": "24/08/2024 20:56:56",
        "date": "24/08/2024",
        "time": "20:56:56",
        "logged_human_time": "4 hours",
        "logged_seconds": 14400,
        "jira_id": "FOO-10238",
        "jira_title": "October 2024"
    },
    {
        "uuid": "64469ae4-325d-4fae-833d-7b3c61e4d8ce",
        "date_time": "24/08/2024 20:28:38",
        "date": "24/08/2024",
        "time": "20:28:38",
        "logged_human_time": "1 hour",
        "logged_seconds": 3600,
        "jira_id": "FOO-10468",
        "jira_title": "January 2025"
    }
]
for item in items:
    date_time = datetime.strptime(item["date_time"], "%d/%m/%Y %H:%M:%S")
    LoggedItem.add(
        uuid=item["uuid"],
        date_time=date_time,
        seconds=item["logged_seconds"],
        seconds_human=item["logged_human_time"],
        jira_id=item["jira_id"],
        jira_title=item["jira_title"],
    )
