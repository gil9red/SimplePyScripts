#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Как подружить sqlalchemy + cx_Oracle на Windows 7:
# https://gist.github.com/gil9red/5c366eede5ecb134df99162265cf9440


import sqlalchemy


USER = "USER"
PASS = "PASS"
HOST = "HOST"
PORT = "1521"
SERVICE_NAME = "SERVICE_NAME"

# Example: 'oracle://scott:123@localhost:1521/myservicename
DB_URL = f"oracle://{USER}:{PASS}@{HOST}:{PORT}/{SERVICE_NAME}"


engine = sqlalchemy.create_engine(DB_URL, echo=True)
connection = engine.connect()

result = connection.execute("select * from RDX_AC_USER order by name")
for row in result:
    print(row)

connection.close()
