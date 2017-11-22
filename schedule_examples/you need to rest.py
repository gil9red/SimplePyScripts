#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# Без этого не будут виджеты работать
app = QApplication([])


# 60 * 1000 * 10 -- 10 minutes
def show_message(text, timeout=60 * 1000 * 10):
    print('show_message: "{}"'.format(text))

    msg = QMessageBox()
    msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
    msg.setWindowTitle("Информация")
    msg.setText("<p align='center'>{}<.p>".format(text))
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)

    # font = msg.font()
    # or:
    font = QFont()
    font.setFamily('Times')
    font.setPointSize(50)
    msg.setFont(font)

    QTimer.singleShot(timeout, msg.close)

    msg.exec()


# pip install schedule
import schedule
schedule.every().day.at("11:00").do(lambda: show_message("Пора в столовку"))
schedule.every().day.at("13:00").do(lambda: show_message("Иди прогуляйся"))
schedule.every().day.at("15:00").do(lambda: show_message("Иди прогуляйся"))
schedule.every().day.at("17:00").do(lambda: show_message("Иди прогуляйся"))
schedule.every().day.at("19:00").do(lambda: show_message("Вали домой"))


print('Jobs:')
for job in schedule.jobs:
    print('    ' + str(job))

print()

while True:
    schedule.run_pending()

    import time
    time.sleep(1)
