#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery


db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('database.sqlite')
if not db.open():
    raise Exception(db.lastError().text())

TABLE = 'word2emoji'
query = QSqlQuery()
query.exec(f'SELECT COUNT(*) FROM {TABLE}')
query.next()
TABLE_ROW_COUNT = query.value(0)


def update_window_title():
    mw.setWindowTitle(f'{model.rowCount()} / {TABLE_ROW_COUNT}')


app = QApplication([])

model = QSqlQueryModel()
model.rowsInserted.connect(update_window_title)
model.setQuery(f"SELECT * FROM {TABLE}")

mw = QTableView()
mw.setEditTriggers(QTableView.NoEditTriggers)
mw.setModel(model)
mw.resize(600, 480)
mw.show()

update_window_title()

app.exec()
