#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


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
    def get_by_date(cls, date: str) -> Optional["LoggedDate"]:
        return cls.select_one(where=dict(date=date))

    @classmethod
    def add(cls, date: str) -> "LoggedDate":
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
    logged: Logged
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


for model in BaseModel.get_inherited_models():
    model.create_table()


date = "2024-09-23"
print(Logged.get_by_date(date))
print(Logged.add(date))
print(Logged.add(date))
print(Logged.get_by_date(date))
print()

for obj in Logged.select():
    print(obj)
