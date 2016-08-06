#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
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
        # TODO: ловить исключения
        try:
            from get_user_and_deviation_hours import get_user_and_deviation_hours
            name, deviation_hours = get_user_and_deviation_hours()

            ok = deviation_hours[0] != '-'
            title = 'Переработка' if ok else 'Недоработка'
            text = name + ': ' + title.lower() + ' ' + deviation_hours
            icon = QSystemTrayIcon.Information if ok else QSystemTrayIcon.Warning
            print(text)

            tray.showMessage(title, text, icon)

        except Exception as e:
            print(e)

    tray.activated.connect(tray_message)

    app.exec()
