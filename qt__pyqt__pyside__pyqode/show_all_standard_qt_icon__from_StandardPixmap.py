#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QMessageBox, QGridLayout, QPushButton, QStyle, QWidget


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    import traceback

    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)
    QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


if __name__ == '__main__':
    app = QApplication([])
    style = app.style()

    enum_items_standard_pixmap = [x for x in dir(QStyle) if x.startswith('SP_')]

    mw = QWidget()
    mw.setWindowTitle('show_all_standard_qt_icon__from_StandardPixmap')

    layout = QGridLayout()

    max_column = 4
    for i, enum_name in enumerate(enum_items_standard_pixmap):
        enum_value = getattr(QStyle, enum_name)
        icon = style.standardIcon(enum_value)

        button = QPushButton(icon, enum_name)

        row = i // max_column
        col = i % max_column
        layout.addWidget(button, row, col)

    mw.setLayout(layout)
    mw.show()

    app.exec()
