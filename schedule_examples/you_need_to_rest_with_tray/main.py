#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import sys
import traceback
import re

from pathlib import Path

# pip install schedule
import schedule

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# 60 * 1000 * 10 -- 10 minutes
def show_message(text, timeout=60 * 1000 * 10):
    print(f'show_message: {text!r}')

    msg = QMessageBox()
    msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
    msg.setWindowTitle("Информация")
    msg.setText(f"<p align='center'>{text}<.p>")
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


class RunSchedulerThread(QThread):
    about_show_message = pyqtSignal(str)
    about_description = pyqtSignal(str)

    def run(self):
        schedule.every().day.at("11:00").do(self.about_show_message.emit, "Пора в столовку")
        schedule.every().day.at("13:00").do(self.about_show_message.emit, "Иди прогуляйся")
        schedule.every().day.at("15:00").do(self.about_show_message.emit, "Иди прогуляйся")
        schedule.every().day.at("17:00").do(self.about_show_message.emit, "Иди прогуляйся")
        schedule.every().day.at("17:09").do(self.about_show_message.emit, "Иди прогуляйся")
        schedule.every().day.at("19:00").do(self.about_show_message.emit, "Вали домой")

        description = 'Jobs:\n'
        description_gui = ''
        for job in schedule.jobs:
            description += '    ' + str(job) + "\n"
            description_gui += str(job) + "\n"

        # Костыль для показа сообщения вида "Every 1 day at 11:00:00"
        pattern = re.compile(r' do <lambda>\(\) \(last run: .+?, next run: .+?\)')
        description = pattern.sub('', description)
        description_gui = pattern.sub('', description_gui)

        print(description)

        while True:
            schedule.run_pending()
            time.sleep(1)

            next_job_time = schedule.next_run().time()
            idle_secs = int(schedule.idle_seconds())

            local_description_gui = description_gui
            local_description_gui += '\n\n'
            local_description_gui += f'Следующий перерыв будет в {next_job_time}, осталось {idle_secs} секунд'
            self.about_description.emit(local_description_gui)


DIR = Path(__file__).resolve().parent
TRAY_ICON = str(DIR / 'rest_32x32.png')


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    tray = QSystemTrayIcon(QIcon(TRAY_ICON))

    menu = QMenu()

    widget_info = QPlainTextEdit()
    widget_info.setReadOnly(True)
    widget_info.setFixedSize(220, 180)
    widget_info_action = QWidgetAction(app)
    widget_info_action.setDefaultWidget(widget_info)

    button_box_layout = QHBoxLayout()
    button_box_layout.setContentsMargins(0, 0, 0, 0)
    button_box_layout.setSpacing(0)

    button = QPushButton('Hide')
    button.clicked.connect(menu.hide)
    button_box_layout.addWidget(button)

    button = QPushButton('Quit')
    button.clicked.connect(quit)
    button_box_layout.addWidget(button)

    button_box = QWidget()
    button_box.setLayout(button_box_layout)

    button_box_action = QWidgetAction(app)
    button_box_action.setDefaultWidget(button_box)

    menu.addAction(widget_info_action)
    menu.addAction(button_box_action)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda x: menu.exec(tray.geometry().center()))

    tray.setToolTip('Уведомления об отдыхе')
    tray.show()

    # Для работы с schedule нужен свой цикл, наподобии цикла, создаваемого app.exec()
    # И чтобы они друг другу не мешали, schedule был отправлен в отдельный поток, но виджеты могут существовать
    # только в главном потоке, поэтому от потока будет идти сигнал, который в главном потоке вызовет окно с сообщением
    thread = RunSchedulerThread()
    thread.about_show_message.connect(show_message)
    thread.about_description.connect(widget_info.setPlainText)
    thread.start()

    app.exec()
