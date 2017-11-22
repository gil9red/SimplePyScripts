#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# Без этого не будут виджеты работать
app = QApplication([])


# 60 * 1000 * 10 -- 10 minutes
def show_message(text, timeout=60 * 1000 * 30):
    print('show_message: "{}"'.format(text))

    msg_box = QMessageBox()
    msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
    msg_box.setWindowTitle("Информация")
    msg_box.setText(text)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)

    QTimer.singleShot(timeout, msg_box.close)

    msg_box.exec()


# pip install schedule
import schedule
schedule.every().day.at("11:00").do(lambda: show_message("Пора в столовку сходить"))
schedule.every().day.at("13:00").do(lambda: show_message("Подними жопу и прогуляйся"))
schedule.every().day.at("15:00").do(lambda: show_message("Подними жопу и прогуляйся"))
schedule.every().day.at("17:00").do(lambda: show_message("Подними жопу и прогуляйся"))
schedule.every().day.at("19:00").do(lambda: show_message("Вали домой"))


print('Jobs:')
for job in schedule.jobs:
    print('    ' + str(job))

print()

while True:
    schedule.run_pending()

    import time
    time.sleep(1)
