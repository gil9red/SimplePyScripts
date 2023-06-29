#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import os
import shutil
import sqlite3

from typing import NamedTuple

from bs4 import BeautifulSoup
import requests


class CrashStatistics(NamedTuple):
    date: str
    dtp: int

    died: int
    children_died: int

    wounded: int
    wounded_children: int


def get_crash_statistics() -> CrashStatistics:
    """
    Example: CrashStatistics(date='27.08.2018', dtp=424, died=40, children_died=1, wounded=549, wounded_children=81)

    :return: Dict
    """

    rs = requests.get("https://гибдд.рф/")

    root = BeautifulSoup(rs.content, "html.parser")
    table = root.select_one("table.b-crash-stat")

    # Example: "АВАРИЙНОСТЬ НА ДОРОГАХ РОССИИ ЗА 27.08.2018"
    table_title = table.select_one("th").text.strip()

    date_str = table_title.replace("АВАРИЙНОСТЬ НА ДОРОГАХ РОССИИ ЗА ", "")

    # Example: {'ДТП': 424, 'Погибли': 40, 'Погибло детей': 1, 'Ранены': 549, 'Ранено детей': 81}
    key_by_value = dict()

    for tr in table.select("tr"):
        td_list = tr.select("td")
        if not td_list:
            continue

        k, v = [td.text.strip() for td in td_list]
        key_by_value[k] = int(v)

    return CrashStatistics(
        date_str,
        key_by_value["ДТП"],
        key_by_value["Погибли"],
        key_by_value["Погибло детей"],
        key_by_value["Ранены"],
        key_by_value["Ранено детей"],
    )


DB_FILE_NAME = "db.sqlite"


def create_connect(fields_as_dict=False, trace_sql=False) -> sqlite3.Connection:
    connect = sqlite3.connect(DB_FILE_NAME)

    if trace_sql:
        my_print = lambda text: print("SQL: " + text.strip())
        connect.set_trace_callback(my_print)

    if fields_as_dict:
        connect.row_factory = sqlite3.Row

    return connect


def init_db():
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.execute(
            """
            CREATE TABLE IF NOT EXISTS CrashStatistics (
                id                INTEGER  PRIMARY KEY,
                date              TEXT     NOT NULL,
                dtp               INTEGER  NOT NULL,
                died              INTEGER  NOT NULL,
                children_died     INTEGER  NOT NULL,
                wounded           INTEGER  NOT NULL,
                wounded_children  INTEGER  NOT NULL,
                
                CONSTRAINT date_unique UNIQUE (date)
            );
        """
        )

        connect.commit()


def db_create_backup(backup_dir="backup"):
    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(dt.datetime.today().date()) + ".sqlite"
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


def append_crash_statistics_db(crash_statistics: CrashStatistics = None):
    db_create_backup()

    if not crash_statistics:
        crash_statistics = get_crash_statistics()

    print(f"Append: {crash_statistics}")

    with create_connect() as connect:
        sql = """
        INSERT OR IGNORE INTO CrashStatistics 
            (date, dtp, died, children_died, wounded, wounded_children) 
        VALUES 
            (:date, :dtp, :died, :children_died, :wounded, :wounded_children)
        """

        connect.execute(sql, crash_statistics._asdict())

        connect.commit()


def get_crash_statistics_list_db() -> list[CrashStatistics]:
    with create_connect() as connect:
        sql = """
        SELECT 
            date, dtp, died, children_died, wounded, wounded_children 
        FROM
            CrashStatistics
        ORDER BY id ASC
        """

        return [CrashStatistics(*row) for row in connect.execute(sql)]


if __name__ == "__main__":
    crash_statistics = get_crash_statistics()
    print(crash_statistics)
    print(crash_statistics._asdict())
    print()

    init_db()

    append_crash_statistics_db()
    print()

    crash_statistics_list = get_crash_statistics_list_db()
    print(
        f"Crash statistics list ({len(crash_statistics_list)}): {crash_statistics_list}"
    )
