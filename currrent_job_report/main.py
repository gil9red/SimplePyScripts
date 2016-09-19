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


import os.path
TRAY_ICON = os.path.join(os.path.dirname(__file__), 'favicon.ico')


import datetime

from get_user_and_deviation_hours import get_user_and_deviation_hours


from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *


class JobReportWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.last_day = None
        self.text = None
        self.ok = None

        self.info = QLabel()

        self.refresh_button = QToolButton()
        self.refresh_button.setText('Refresh')
        self.refresh_button.setAutoRaise(True)
        self.refresh_button.clicked.connect(lambda x: self.reread() or self.refresh())

        self.quit_button = QToolButton()
        self.quit_button.setText('Quit')
        self.quit_button.setAutoRaise(True)
        self.quit_button.clicked.connect(QApplication.instance().quit)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.info)
        layout.addSpacing(10)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.quit_button)

        self.timer = QTimer()
        self.timer.setInterval(1000 * 60 * 60)
        self.timer.timeout.connect(self.refresh)

        self.setLayout(layout)

        self.refresh()

    def reread(self):
        print('reread')

        name, deviation_hours = get_user_and_deviation_hours()

        self.ok = deviation_hours[0] != '-'
        self.text = name + '\n' + ('Переработка' if self.ok else 'Недоработка') + ' ' + deviation_hours

    def refresh(self):
        print('refresh')

        today = datetime.date.today()
        if self.last_day != today:
            self.last_day = today
            self.reread()

        print(self.text)
        self.info.setText('Check for {}\n{}'.format(self.last_day.strftime('%d/%m/%Y'), self.text))

    def paintEvent(self, event):
        super().paintEvent(event)

        color = Qt.green if self.ok else Qt.red

        painter = QPainter(self)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QApplication([])

    tray = QSystemTrayIcon(QIcon(TRAY_ICON))

    job_report_widget = JobReportWidget()
    job_report_widget_action = QWidgetAction(job_report_widget)
    job_report_widget_action.setDefaultWidget(job_report_widget)

    menu = QMenu()
    menu.addAction(job_report_widget_action)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda x: menu.exec(tray.geometry().center()))

    tray.setToolTip('Compass Plus. Рапорт учета рабочего времени')
    tray.show()

    app.exec()
