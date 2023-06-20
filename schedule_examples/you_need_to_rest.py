#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install schedule
import schedule

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# 60 * 1000 * 10 -- 10 minutes
def show_message(text, timeout=60 * 1000 * 10):
    print(f"show_message: {text!r}")

    msg = QMessageBox()
    msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
    msg.setWindowTitle("Информация")
    msg.setText(f"<p align='center'>{text}<.p>")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)

    font = msg.font()
    font.setFamily("Times")
    font.setPointSize(50)
    msg.setFont(font)

    QTimer.singleShot(timeout, msg.close)

    msg.exec()


if __name__ == "__main__":
    app = QApplication([])

    schedule.every().day.at("11:00").do(show_message, "Пора в столовку")
    schedule.every().day.at("13:00").do(show_message, "Иди прогуляйся")
    schedule.every().day.at("15:00").do(show_message, "Иди прогуляйся")
    schedule.every().day.at("17:00").do(show_message, "Иди прогуляйся")
    schedule.every().day.at("19:00").do(show_message, "Вали домой")

    print("Jobs:")
    for job in schedule.jobs:
        print("    " + str(job))

    print()

    while True:
        schedule.run_pending()
        time.sleep(1)
