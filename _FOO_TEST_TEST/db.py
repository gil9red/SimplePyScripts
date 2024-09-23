#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, fields
from typing import Any, Optional

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
    def select(cls, where: dict[str, Any] = None):  # TODO: typing генератор
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
            FROM {cls.__name__}
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


@dataclass
class LoggedDate(BaseModel):
    id: int
    date: str
    total_seconds: int
    total_seconds_human: str

    @classmethod
    def create_table(cls):
        QSqlQuery(
            """
            CREATE TABLE IF NOT EXISTS LoggedDate(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date VARCHAR(10) UNIQUE,
                total_seconds INTEGER DEFAULT 0,
                total_seconds_human TEXT
            )
            """
        ).exec()

    @classmethod
    def get_by_date(cls, date: str) -> Optional["LoggedDate"]:
        return next(
            cls.select(dict(date=date)),
            None
        )

    @classmethod
    def add(cls, date: str) -> "LoggedDate":
        # Если уже есть
        if obj := cls.get_by_date(date):
            return obj

        query = QSqlQuery()
        query.prepare("INSERT INTO LoggedDate (date) VALUES (:date)")
        query.bindValue(":date", date)
        query.exec()

        return cls.get_by_date(date)


@dataclass
class LoggedDateItem:
    uuid: str
    logged_date: LoggedDate
    time: str
    seconds: int
    seconds_human: str
    jira_id: str
    jira_title: str

    @classmethod
    def create_table(cls):
        QSqlQuery(
            """
            CREATE TABLE IF NOT EXISTS LoggedDateItem(
                uuid TEXT PRIMARY KEY,
                logged_date_id INTEGER,
                time VARCHAR(8),
                seconds INTEGER DEFAULT 0,
                seconds_human TEXT,
                jira_id TEXT,
                jira_title TEXT,
                
                FOREIGN KEY (logged_date_id) REFERENCES LoggedDate (id) ON DELETE CASCADE
            )
            """
        ).exec()


LoggedDate.create_table()
LoggedDateItem.create_table()


date = "2024-09-23"
print(LoggedDate.get_by_date(date))
print(LoggedDate.add(date))
print(LoggedDate.add(date))
print(LoggedDate.get_by_date(date))
print()

for obj in LoggedDate.select():
    print(obj)
