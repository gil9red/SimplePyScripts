#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection


DIR = os.path.dirname(__file__)
DB_FILE_NAME = "sqlite:///" + os.path.join(DIR, "database")

# Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
engine = create_engine(
    DB_FILE_NAME,
    # echo=True,
    pool_recycle=7200,
)

inspector = reflection.Inspector.from_engine(engine)

table_names = inspector.get_table_names()
for table in table_names:
    columns = [column_info["name"] for column_info in inspector.get_columns(table)]
    print("{}: {}".format(table, ", ".join(columns)))

    for row in engine.execute("select * from {}".format(table)):
        print(row.values())
