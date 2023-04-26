#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import sqlite3
import os

from bs4 import BeautifulSoup


def build_sql_table(table_name: str, format_fields_of_table: [dict]) -> str:
    """
    Функция по метаданным о полях сгенерирует SQLite таблицу например:
        CREATE TABLE IF NOT EXISTS BANKS (
            VERSION INTEGER,
            ERASED INTEGER,
            ID INTEGER PRIMARY KEY,
            PARENT_ID INTEGER,
            PP_CODE TEXT,
            BIC TEXT,
            NAME TEXT,
            CITY_HEAD TEXT,
            ADDRESS1 TEXT,
            ADDRESS2 TEXT,
            ADDRESS3 TEXT,
            ADDRESS4 TEXT,
            PHONE TEXT,
            NAME_RUS TEXT,
            COUNTRY INTEGER,
            DELETED INTEGER,
            CITY_LAT TEXT,
            ADDR_LAT TEXT,
            CONTACT INTEGER,
            REGION INTEGER,
            IS_KFM INTEGER,
            IS_ONLINE INTEGER,
            CAN_REVOKE INTEGER,
            CAN_CHANGE INTEGER,
            GET_MONEY INTEGER,
            SEND_CURR TEXT,
            REC_CURR TEXT,
            CO_IN_RUR INTEGER,
            CO_IN_USD INTEGER,
            CO_IN_EUR INTEGER,
            CO_OUT_RUR INTEGER,
            CO_OUT_USD INTEGER,
            CO_OUT_EUR INTEGER,
            ATTR_GRPS TEXT,
            SCEN_ID INTEGER,
            CITY_ID INTEGER,
            LOGO_ID INTEGER,
            UNIQUE_TRN INTEGER,
            METRO INTEGER
        );

    """

    def build_field_table(format_field: dict, indent=" " * 4) -> str:
        field_name = format_field["attrname"]

        field_type = "TEXT"
        if format_field["fieldtype"] == "i4":
            field_type = "INTEGER"

            if field_name.upper() == "ID":
                field_type += " PRIMARY KEY"

        return indent + "{} {}".format(field_name, field_type)

    fields_list = [
        build_field_table(format_field) for format_field in format_fields_of_table
    ]

    table = """\
CREATE TABLE IF NOT EXISTS {table_name} (
{fields_list}
);
""".format(
        table_name=table_name.upper(), fields_list=",\n".join(fields_list)
    )

    return table


def build_sql_rows_data_table(table_name: str, rows_of_table: [dict]) -> str:
    """
    Функция по данным о полях сгенерирует запрос для добавления их в таблицу::
        INSERT OR IGNORE INTO COUNTRY (CODE,ERASED,ID,IS_EUR,IS_FATF,IS_RUR,IS_USD,NAME,NAME_LAT,PP_CODE,REC_CURR,SEND_CURR,VERSION) VALUES ('RU','0','0','1','1','1','1','Российская Федерация','RUSSIAN FEDERATION','CDPA  ','RUR;USD;EUR;','RUR;USD;EUR;','15');
        INSERT OR IGNORE INTO COUNTRY (CODE,ERASED,ID,IS_EUR,IS_FATF,IS_RUR,IS_USD,NAME,NAME_LAT,REC_CURR,SEND_CURR,VERSION) VALUES ('TJ','0','762','1','0','1','1','ТАДЖИКИСТАН','TAJIKISTAN','RUR;USD;EUR;','USD;EUR;','15');
        INSERT OR IGNORE INTO COUNTRY (CODE,ERASED,ID,IS_EUR,IS_FATF,IS_RUR,IS_USD,NAME,NAME_LAT,REC_CURR,SEND_CURR,VERSION) VALUES ('BY','0','112','1','0','1','1','БЕЛАРУСЬ','BELARUS','RUR;USD;EUR;','','15');
        INSERT OR IGNORE INTO COUNTRY (CODE,ERASED,ID,IS_EUR,IS_FATF,IS_RUR,IS_USD,NAME,NAME_LAT,REC_CURR,SEND_CURR,VERSION) VALUES ('KZ','0','398','1','0','1','1','КАЗАХСТАН','KAZAKHSTAN','RUR;USD;EUR;','','15');
        INSERT OR IGNORE INTO COUNTRY (CODE,ERASED,ID,IS_EUR,IS_FATF,IS_RUR,IS_USD,NAME,NAME_LAT,REC_CURR,SEND_CURR,VERSION) VALUES ('UZ','0','860','1','0','1','1','УЗБЕКИСТАН','UZBEKISTAN','RUR;USD;EUR;','','15');

    """

    def build_insert(row_of_table: dict) -> str:
        keys = sorted(key for key in row_of_table.keys())

        # return "INSERT OR REPLACE INTO {table_name} ({fields}) VALUES ({values});".format(
        return (
            "INSERT OR IGNORE INTO {table_name} ({fields}) VALUES ({values});".format(
                table_name=table_name.upper(),
                fields=",".join(key.upper() for key in keys),
                values=",".join(
                    repr(row_of_table[key]).replace('\\"', "").replace("\\'", "")
                    for key in keys
                ),
            )
        )

    return "\n".join(build_insert(row_data.attrs) for row_data in rows_of_table)


def create_connect():
    return sqlite3.connect("database.sqlite")


def create_table(
    table_name: str, sql_table: str, sql_table_data_rows: str, drop_table=False
):
    # Создание таблицы
    connect = create_connect()
    try:
        if drop_table:
            connect.execute("DROP TABLE IF EXISTS ?;", (table_name,))

        connect.execute(sql_table)
        connect.executescript(sql_table_data_rows)

        connect.commit()

    finally:
        connect.close()


if __name__ == "__main__":
    for file_name in glob.glob("contact_dicts/*.xml"):
        table_name = os.path.splitext(os.path.basename(file_name))[0]

        print("Append {} from {}".format(table_name, file_name))

        root = BeautifulSoup(open(file_name, "rb"), "lxml")

        format_fields_of_dict = [
            row for row in root.select("metadata > fields > field")
        ]
        rows_of_dict = [row for row in root.select("rowdata > row")]

        sql_table = build_sql_table(table_name, format_fields_of_dict)
        sql_table_data_rows = build_sql_rows_data_table(table_name, rows_of_dict)
        # print(sql_table + "\n\n" + sql_table_data_rows)

        print("  Append {} rows\n".format(len(rows_of_dict)))
        create_table(table_name, sql_table, sql_table_data_rows)

        # print()
        # print("Test sql")
        # connect = create_connect()
        #
        # import sqlite3
        # connect.row_factory = sqlite3.Row
        #
        # try:
        #     for country in connect.execute('SELECT * FROM {}'.format(table_name)).fetchall():
        #         print(dict(country))
        #
        # finally:
        #     connect.close()
        #
        # print('\n')
