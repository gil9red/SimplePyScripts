#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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


class RunSchedulerThread(QThread):
    about_show_message = pyqtSignal(str)
    about_description = pyqtSignal(str)

    def run(self):
        # pip install schedule
        import schedule
        schedule.every().day.at("11:00").do(lambda: self.about_show_message.emit("Пора в столовку"))
        schedule.every().day.at("13:00").do(lambda: self.about_show_message.emit("Иди прогуляйся"))
        schedule.every().day.at("15:00").do(lambda: self.about_show_message.emit("Иди прогуляйся"))
        schedule.every().day.at("17:00").do(lambda: self.about_show_message.emit("Иди прогуляйся"))
        schedule.every().day.at("19:00").do(lambda: self.about_show_message.emit("Вали домой"))

        description = 'Jobs:\n'
        for job in schedule.jobs:
            description += '    ' + str(job) + "\n"

        # Костыль для показа сообщения вида "Every 1 day at 11:00:00"
        import re
        description = re.sub(r' do <lambda>\(\) \(last run: .+?, next run: .+?\)', '', description)

        print(description)
        self.about_description.emit(description)

        while True:
            schedule.run_pending()

            import time
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    style = app.style()
    icon = style.standardIcon(QStyle.SP_BrowserReload)

    tray = QSystemTrayIcon(icon)

    menu = QMenu()

    widget_info = QPlainTextEdit()
    widget_info.setReadOnly(True)
    widget_info.setFixedSize(200, 130)
    widget_info_action = QWidgetAction(widget_info)
    widget_info_action.setDefaultWidget(widget_info)

    menu.addAction(widget_info_action)

    action_quit = menu.addAction('Quit')
    action_quit.triggered.connect(quit)

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
