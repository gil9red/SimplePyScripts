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

# TODO:
DIR = 'exports'
import os


def save_to_csv(table_name, columns, rows):
    file_name = table_name + '.csv'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    file_name = os.path.join(DIR, file_name)

    import csv
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(columns)
        for row in rows:
            csv_writer.writerow(row)


def save_to_json(table_name, columns, rows, pretty=True):
    file_name = table_name + ('_mini' if not pretty else '') + '.json'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    file_name = os.path.join(DIR, file_name)

    from collections import OrderedDict
    import json
    with open(file_name, 'w', encoding='utf-8') as f:
        new_rows = [OrderedDict(zip(columns, row)) for row in rows]
        json.dump(new_rows, f, indent=4 if pretty else None)


def save_to_xml(table_name, columns, rows, pretty=True):
    file_name = table_name + ('_mini' if not pretty else '') + '.xml'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    file_name = os.path.join(DIR, file_name)

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

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(doc.toprettyxml() if pretty else doc.toxml())


def save_to_html(table_name, columns, rows):
    file_name = table_name + '.html'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    file_name = os.path.join(DIR, file_name)

    HTML_TABLE_TEMPLATE = """
<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="utf-8">
            <title>{0}</title>
        </head>
        <body>
            <table border="1">
                <caption>{0}</caption>
                {1}
                {2}
            </table>
        </body>
    </html>
"""

    table_header = "<tr>" + ''.join("<th>{}</th>".format(column) for column in columns) + "</tr>"

    table_rows = list()
    for row in rows:
        table_rows.append("<tr>" + ''.join("<td>{}</td>".format(field) for field in row) + "</tr>")

    table_rows = '\n'.join(table_rows)

    with open(file_name, 'w', encoding='utf-8') as f:
        html = HTML_TABLE_TEMPLATE.format(table_name, table_header, table_rows)
        f.write(html)


if __name__ == '__main__':
    table_name, columns, rows = get_table_database_info('database')

    save_to_csv(table_name, columns, rows)

    save_to_json(table_name, columns, rows)
    save_to_json(table_name, columns, rows, pretty=False)

    save_to_xml(table_name, columns, rows)
    save_to_xml(table_name, columns, rows, pretty=False)

    save_to_html(table_name, columns, rows)
