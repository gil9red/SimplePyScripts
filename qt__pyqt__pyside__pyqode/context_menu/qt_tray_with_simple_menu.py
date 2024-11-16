#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QSystemTrayIcon, QStyle, QMenu, QMessageBox, QWidget


app = QApplication([])
# app.setQuitOnLastWindowClosed(False)

mw = QWidget()
mw.show()

icon = app.style().standardIcon(QStyle.SP_DirOpenIcon)
# OR
# icon = QIcon('favicon.ico')

tray = QSystemTrayIcon(icon)

menu = QMenu()

menu_about = menu.addMenu("About")
action_about = menu_about.addAction("About")
action_about.triggered.connect(
    lambda: QMessageBox.information(None, "Info", "Hello World!")
)

action_about_qt = menu_about.addAction("About Qt")
action_about_qt.triggered.connect(lambda: QMessageBox.aboutQt(None))

menu.addSeparator()
action_quit = menu.addAction("Quit")
action_quit.triggered.connect(app.quit)

tray.setContextMenu(menu)


def on_tray_activated(reason: QSystemTrayIcon.ActivationReason):
    if reason == QSystemTrayIcon.ActivationReason.Context:
        return

    mw.setVisible(not mw.isVisible())


tray.activated.connect(on_tray_activated)

tray.show()

app.exec()
