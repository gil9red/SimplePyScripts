#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import sqlite3
from typing import List


DB_FILE_NAME = 'database.sqlite'

SQL_INSERT = "INSERT INTO Water (cold, hot) VALUES (?, ?)"
SQL_UPDATE = "UPDATE Water SET date = date('now', 'localtime'), cold = ?, hot = ? WHERE id = ?"


def create_connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE_NAME)


def init_db():
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.execute('''
            CREATE TABLE IF NOT EXISTS Water (
                id INTEGER PRIMARY KEY,
                date DATE DEFAULT(date('now', 'localtime')) NOT NULL,
                cold INTEGER NOT NULL,
                hot INTEGER NOT NULL
            );
        ''')


def db_create_backup(backup_dir='backup'):
    from datetime import datetime
    file_name = str(datetime.today().date()) + '.sqlite'

    import os
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    file_name = os.path.join(backup_dir, file_name)

    import shutil
    shutil.copy(DB_FILE_NAME, file_name)


def get_last(date: DT.date = None) -> int:
    if date is None:
        date = DT.date.today()

    yyyymm = date.strftime('%Y%m')

    connect = create_connect()
    result = connect.execute(
        "SELECT id FROM Water WHERE strftime('%Y%m', Water.date) = ? ORDER BY id DESC", [yyyymm]
    ).fetchone()
    return -1 if result is None else result[0]


def delete_last():
    with create_connect() as connect:
        last_id = get_last()
        connect.execute("DELETE FROM Water WHERE id = ?", [last_id])


def is_exist(date: DT.date = None) -> bool:
    return get_last(date) != -1


def add(value_cold: int, value_hot: int, forced=False) -> bool:
    with create_connect() as connect:
        # При forced либо будет добавлена запись за месяц, либо обновлена
        if forced:
            id_ = get_last()
            if id_ == -1:
                connect.execute(SQL_INSERT, (value_cold, value_hot))
            else:
                connect.execute(SQL_UPDATE, (value_cold, value_hot, id_))

        else:
            if is_exist():
                return False

            connect.execute(SQL_INSERT, (value_cold, value_hot))

    db_create_backup()

    return True


def get_all(reversed=True) -> List[dict]:
    sql = 'SELECT id, date, cold, hot FROM Water ORDER BY ID ' + ('DESC' if reversed else 'ASC')
    connect = create_connect()
    connect.row_factory = sqlite3.Row
    return connect.execute(sql).fetchall()


if __name__ == '__main__':
    init_db()

    # # Only for test
    # add(111, 222)
    # add(555, 666, forced=True)
    # with create_connect() as connect:
    #     connect.execute('DELETE FROM Water')

    for row in get_all():
        print(f"#{row['id']} date={row['date']} cold={row['cold']} hot={row['hot']}")
