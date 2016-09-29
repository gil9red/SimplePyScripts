#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Script for exporting from sqlite database file to csv, json, xml and html files."""


def get_table_database_info(file_name, table_name=None):
    """
    Функция подключается к файлу базы данных sqlite и возвращает кортеж из
    строки с названием таблицы, списка столбцов таблицы и списка строк. Каждая строка -- список значений столбцов.

    Если table_name не указано, будет использоваться первая попавшаяся таблица базы.

    """

    DB_FILE_NAME = 'sqlite:///' + file_name

    from sqlalchemy import create_engine
    engine = create_engine(
        DB_FILE_NAME,
        # echo=True,
    )

    from sqlalchemy.engine import reflection
    inspector = reflection.Inspector.from_engine(engine)

    # Если не указана таблица базы, то берем первую попавшуюся
    if not table_name:
        table_names = inspector.get_table_names()
        if not table_names:
            raise Exception("In the database table not found")

        table_name = table_names[0]

    columns = [column_info['name'] for column_info in inspector.get_columns(table_name)]

    rows = list()
    for row in engine.execute("select * from {}".format(table_name)):
        rows.append(row.values())

    return table_name, columns, rows


def save_to_csv(table_name, columns, rows):
    import csv
    with open(table_name + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(columns)
        for row in rows:
            csv_writer.writerow(row)


def save_to_json(table_name, columns, rows):
    from collections import OrderedDict
    import json
    with open(table_name + '.json', 'w', encoding='utf-8') as f:
        new_rows = [OrderedDict(zip(columns, row)) for row in rows]
        json.dump(new_rows, f, indent=4)

    with open(table_name + '_mini.json', 'w', encoding='utf-8') as f:
        new_rows = [OrderedDict(zip(columns, row)) for row in rows]
        json.dump(new_rows, f)


def save_to_xml(table_name, columns, rows):
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()
    doc = impl.createDocument(None, table_name, None)
    root = doc.documentElement

    from collections import OrderedDict
    for employee in [OrderedDict(zip(columns, row)) for row in rows]:
        employee_element = doc.createElement('Employee')
        root.appendChild(employee_element)

        for field, value in employee.items():
            field_element = doc.createElement(field)
            field_element.appendChild(doc.createTextNode(value))

            employee_element.appendChild(field_element)

    with open(table_name + '.xml', 'w', encoding='utf-8') as f:
        f.write(doc.toprettyxml())

    with open(table_name + '_mini.xml', 'w', encoding='utf-8') as f:
        f.write(doc.toxml())
s

if __name__ == '__main__':
    table_name, columns, rows = get_table_database_info('database')

    save_to_csv(table_name, columns, rows)
    save_to_json(table_name, columns, rows)
    save_to_xml(table_name, columns, rows)
