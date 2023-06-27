#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import string

from PyQt5.QtWidgets import (
    QApplication,
    QListView,
    QTableView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
)
from PyQt5.QtGui import QPainter, QPalette, QFontMetrics
from PyQt5.QtCore import Qt, QSize, QRect, QModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel


# SOURCE: https://stackoverflow.com/a/5346900/5909792
class ListViewDelegate(QStyledItemDelegate):
    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        opt = option
        self.initStyleOption(opt, index)

        line_id = str(index.model().data(index.model().index(index.row(), 0)))
        line_key = str(index.model().data(index.model().index(index.row(), 1)))
        line_value = str(index.model().data(index.model().index(index.row(), 2)))

        line_id = f"#{line_id}"

        # Draw correct background
        opt.text = ""
        style = opt.widget.style() if opt.widget else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        rect = opt.rect
        cg = QPalette.Normal if opt.state & QStyle.State_Enabled else QPalette.Disabled
        if cg == QPalette.Normal and not (opt.state & QStyle.State_Active):
            cg = QPalette.Inactive

        # # Set pen color
        # if opt.state & QStyle.State_Selected:
        #     painter.setPen(opt.palette.color(cg, QPalette.HighlightedText))
        # else:
        #     painter.setPen(opt.palette.color(cg, QPalette.Text))
        painter.setPen(opt.palette.color(cg, QPalette.Text))

        # Draw 2 lines of text
        font = painter.font()
        font.setBold(True)

        font_metrics = QFontMetrics(font)
        line_id_width = font_metrics.boundingRect(line_id.zfill(3 + 1)).width() + 20

        key_text = "KEY:"
        key_width = font_metrics.boundingRect(key_text).width() + 10

        value_text = "VALUE:"
        value_width = font_metrics.boundingRect(value_text).width() + 10

        kv_width = max(key_width, value_width)

        painter.save()
        painter.setFont(font)

        # Line id
        painter.drawText(
            QRect(rect.left(), rect.top(), line_id_width, rect.height()),
            Qt.AlignCenter,
            line_id,
        )

        # Line 1
        painter.drawText(
            QRect(
                rect.left() + line_id_width,
                rect.top(),
                line_id_width + kv_width,
                rect.height() / 2,
            ),
            opt.displayAlignment,
            key_text,
        )

        # Line 2
        painter.drawText(
            QRect(
                rect.left() + line_id_width,
                rect.top() + rect.height() / 2,
                line_id_width + kv_width,
                rect.height() / 2,
            ),
            opt.displayAlignment,
            value_text,
        )

        painter.restore()

        # Line 1
        painter.drawText(
            QRect(
                rect.left() + line_id_width + kv_width,
                rect.top(),
                rect.width(),
                rect.height() / 2,
            ),
            opt.displayAlignment,
            line_key,
        )

        # Line 2
        painter.drawText(
            QRect(
                rect.left() + line_id_width + kv_width,
                rect.top() + rect.height() / 2,
                rect.width(),
                rect.height() / 2,
            ),
            opt.displayAlignment,
            line_value,
        )

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        result = super().sizeHint(option, index)
        result.setHeight(result.height() * 2)
        return result


db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(":memory:")
db.open()

db.exec(
    """\
    CREATE TABLE IF NOT EXISTS Dict (
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL UNIQUE,
        value TEXT
    );
"""
)

# Fill
for i in range(1000 - 1):
    value = "".join(string.ascii_lowercase[j] for j in map(int, str(i).zfill(3)))
    db.exec(f"INSERT OR IGNORE INTO Dict (key, value) VALUES ({i}, {value!r})")


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300


app = QApplication([])

model = QSqlQueryModel()
model.setQuery("SELECT id, key, value FROM Dict")
model.setHeaderData(0, Qt.Horizontal, "ID")
model.setHeaderData(1, Qt.Horizontal, "KEY")
model.setHeaderData(2, Qt.Horizontal, "VALUE")

list_view = QListView()
list_view.setWindowTitle("QListView")
list_view.setModel(model)
list_view.move(100, 50)
list_view.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
list_view.show()

list_view_2 = QListView()
list_view_2.setWindowTitle("QListView + ItemDelegate")
list_view_2.setItemDelegate(ListViewDelegate())
list_view_2.setModel(model)
list_view_2.move(list_view.geometry().right(), 50)
list_view_2.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
list_view_2.show()

table_view = QTableView()
table_view.setWindowTitle("QTableView")
table_view.setModel(model)
table_view.move(list_view.pos().x(), list_view.geometry().bottom())
table_view.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
table_view.show()

app.exec()
