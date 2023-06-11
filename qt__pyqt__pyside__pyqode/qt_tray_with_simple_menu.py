#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QSystemTrayIcon, QStyle, QMenu, QMessageBox, QWidget


app = QApplication([])
# app.setQuitOnLastWindowClosed(False)

mw = QWidget()
mw.show()

icon = app.style().standardIcon(QStyle.SP_DirOpenIcon)
# icon = QIcon('favicon.ico')

tray = QSystemTrayIcon(icon)

menu = QMenu()
action_settings = menu.addAction("About Qt")
action_settings.triggered.connect(lambda: QMessageBox.aboutQt(None))

action_quit = menu.addAction("Quit")
action_quit.triggered.connect(app.quit)

tray.setContextMenu(menu)
tray.activated.connect(lambda x: menu.exec(tray.geometry().center()))

tray.show()

app.exec()
