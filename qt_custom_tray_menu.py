#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    icon = app.style().standardIcon(QStyle.SP_DirOpenIcon)
    # icon = QIcon('favicon.ico')

    tray = QSystemTrayIcon(icon)

    menu_widget = QLabel('<b>Hello</b>, World!')
    menu_widget_action = QWidgetAction(menu_widget)
    menu_widget_action.setDefaultWidget(menu_widget)

    menu = QMenu()
    menu.addAction(menu_widget_action)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda x: menu.exec(tray.geometry().center()))

    tray.show()

    app.exec()
