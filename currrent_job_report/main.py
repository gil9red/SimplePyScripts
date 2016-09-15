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


import datetime

from get_user_and_deviation_hours import get_user_and_deviation_hours


# TODO: свое меню трея (просто интересно)
# TODO: возможность закрывать программу
if __name__ == '__main__':
    app = QApplication([])

    tray = QSystemTrayIcon(QIcon(TRAY_ICON))
    tray.setToolTip('Compass Plus. Рапорт учета рабочего времени')
    tray.show()

    LAST_DAY = None
    TITLE, TEXT, ICON = None, None, None

    def tray_message(reason=None):
        global LAST_DAY, TITLE, TEXT, ICON

        if LAST_DAY != datetime.date.today().day:
            LAST_DAY = datetime.date.today().day

            name, deviation_hours = get_user_and_deviation_hours()

            ok = deviation_hours[0] != '-'
            TITLE = 'Переработка' if ok else 'Недоработка'
            TEXT = name + ': ' + TITLE.lower() + ' ' + deviation_hours
            ICON = QSystemTrayIcon.Information if ok else QSystemTrayIcon.Warning

        print(TEXT)
        tray.showMessage(TITLE, TEXT, ICON)

    tray.activated.connect(tray_message)

    app.exec()
