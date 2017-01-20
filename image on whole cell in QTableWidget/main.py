#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)
    QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


def create_item(img):
    item = QTableWidgetItem()
    item.setData(Qt.DecorationRole, img)

    return item


class MyDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        rect = option.rect
        img = index.model().data(index, Qt.DecorationRole)

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

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawRect(rect)

        painter.restore()

        # Если хотим что-то дорисовать (например текст)
        # super().paint(painter, option, index)


if __name__ == '__main__':
    app = QApplication([])

    table = QTableWidget()
    table.show()

    headers = ['Normal', 'Delegate']
    table.setHorizontalHeaderLabels(headers)
    table.setColumnCount(len(headers))
    table.setRowCount(3)
    table.verticalHeader().hide()

    pix_1 = QPixmap('favicon_google.png')
    pix_2 = QPixmap('favicon_prog_org.png')
    pix_3 = QPixmap('favicon_google_tr.png')

    table.setItem(0, 0, create_item(pix_1))
    table.setItem(1, 0, create_item(pix_2))
    table.setItem(2, 0, create_item(pix_3))

    table.setItem(0, 1, create_item(pix_1))
    table.setItem(1, 1, create_item(pix_2))
    table.setItem(2, 1, create_item(pix_3))

    table.setItemDelegateForColumn(1, MyDelegate())

    app.exec()
