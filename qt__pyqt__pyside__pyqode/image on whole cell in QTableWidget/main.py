#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print("Error: ", text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


def create_item(img):
    item = QTableWidgetItem()
    item.setData(Qt.DecorationRole, img)

    return item


class MyDelegate_1(QStyledItemDelegate):
    def paint(self, painter, option, index):
        img = index.model().data(index, Qt.DecorationRole)
        if img is None:
            super().paint(painter, option, index)
            return

        rect = option.rect
        w, h = rect.size().width(), rect.size().height()
        img = img.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter.drawPixmap(rect, img)

        item_option = QStyleOptionViewItem(option)
        self.initStyleOption(item_option, index)

        # Обработка при выделении ячейки делегата
        # Рисуем выделение полупрозрачным чтобы было видно нарисованное ранее
        if item_option.state & QStyle.State_Selected:
            color = item_option.palette.color(QPalette.Highlight)
            color.setAlpha(180)

            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawRect(rect)
            painter.restore()

        # Если хотим что-то дорисовать (например текст)
        # super().paint(painter, option, index)


class MyDelegate_2(QStyledItemDelegate):
    def paint(self, painter, option, index):
        img = index.model().data(index, Qt.DecorationRole)
        if img is None:
            super().paint(painter, option, index)
            return

        rect = option.rect
        x, y = rect.x(), rect.y()
        painter.drawPixmap(x, y, img)

        painter.drawPixmap(x + 16, y, img)
        painter.drawPixmap(x + 32, y, img)
        painter.drawPixmap(x + 48, y, img)
        painter.drawPixmap(x + 64, y, img)
        painter.drawPixmap(x + 80, y, img)

        painter.drawPixmap(x, y + 16, img)
        painter.drawPixmap(x + 16, y + 16, img)

        item_option = QStyleOptionViewItem(option)
        self.initStyleOption(item_option, index)

        # Обработка при выделении ячейки делегата
        # Рисуем выделение полупрозрачным чтобы было видно нарисованное ранее
        if item_option.state & QStyle.State_Selected:
            color = item_option.palette.color(QPalette.Highlight)
            color.setAlpha(180)

            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawRect(rect)
            painter.restore()

        # # Если хотим что-то дорисовать (например текст)
        # super().paint(painter, option, index)


if __name__ == "__main__":
    app = QApplication([])

    table = QTableWidget()
    table.setSelectionBehavior(QTableView.SelectRows)
    table.show()
    table.resize(400, 200)

    headers = ["Normal", "Delegate v1", "Delegate v1 (without img)", "Delegate v2"]
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(3)
    table.verticalHeader().hide()

    pix_1 = QPixmap("favicon_google.png")
    pix_2 = QPixmap("favicon_prog_org.png")
    pix_3 = QPixmap("favicon_google_tr.png")

    for col in range(table.columnCount()):
        if col == 2:
            table.setItem(1, col, QTableWidgetItem())
        else:
            table.setItem(0, col, create_item(pix_1))
            table.setItem(1, col, create_item(pix_2))
            table.setItem(2, col, create_item(pix_3))

    delegate_1 = MyDelegate_1()
    delegate_2 = MyDelegate_2()

    table.setItemDelegateForColumn(1, delegate_1)
    table.setItemDelegateForColumn(2, delegate_1)
    table.setItemDelegateForColumn(3, delegate_2)

    app.exec()
