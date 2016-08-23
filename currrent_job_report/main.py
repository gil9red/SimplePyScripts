#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import traceback


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)
    QMessageBox.critical(None, 'Error', text)
    quit()

import sys
sys.excepthook = log_uncaught_exceptions


from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox
from PyQt5.QtGui import QIcon

import os.path
TRAY_ICON = 'favicon.ico'
TRAY_ICON = os.path.join(os.path.dirname(__file__), TRAY_ICON)


# TODO: кэширование
# TODO: свое меню трея (просто интересно)
# TODO: добавить батник сборки в ехе
if __name__ == '__main__':
    app = QApplication([])

    tray = QSystemTrayIcon(QIcon(TRAY_ICON))
    tray.setToolTip('Compass Plus. Рапорт учета рабочего времени')
    tray.show()

    def tray_message(reason=None):
        from get_user_and_deviation_hours import get_user_and_deviation_hours
        name, deviation_hours = get_user_and_deviation_hours()
        print(name)
        print(deviation_hours)

        ok = deviation_hours[0] != '-'
        title = 'Переработка' if ok else 'Недоработка'
        text = name + ': ' + title.lower() + ' ' + deviation_hours
        icon = QSystemTrayIcon.Information if ok else QSystemTrayIcon.Warning
        print(text)

        tray.showMessage(title, text, icon)

    tray.activated.connect(tray_message)

    app.exec()
