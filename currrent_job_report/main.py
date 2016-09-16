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
TRAY_ICON = 'favicon.ico'
TRAY_ICON = os.path.join(os.path.dirname(__file__), TRAY_ICON)


import datetime

from get_user_and_deviation_hours import get_user_and_deviation_hours


from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *


class JobReportWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.last_day = None
        self.title = None
        self.text = None
        self.ok = None

        self.info = QLabel()

        self.refresh_button = QToolButton()
        self.refresh_button.setText('Refresh')
        self.refresh_button.setAutoRaise(True)
        self.refresh_button.clicked.connect(lambda x: self.reread() or self.refresh())

        layout = QVBoxLayout()
        layout.addWidget(self.info)
        layout.addStretch()
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

        self.refresh()

    def reread(self):
        print('reread')

        name, deviation_hours = get_user_and_deviation_hours()

        # TODO: формат вывода сделать получше
        self.ok = deviation_hours[0] != '-'
        self.title = 'Переработка' if self.ok else 'Недоработка'
        self.text = name + ': ' + self.title.lower() + ' ' + deviation_hours

    def refresh(self):
        print('refresh')

        today = datetime.date.today().day
        if self.last_day != today:
            self.last_day = today
            self.reread()

        print(self.text)
        self.info.setText('{}\n{}'.format(self.title, self.text))

    def setVisible(self, val):
        if val:
            self.refresh()

        super().setVisible(val)

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
    menu.addAction('Quit').triggered.connect(app.quit)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda x: menu.exec(tray.geometry().center()))

    tray.setToolTip('Compass Plus. Рапорт учета рабочего времени')
    tray.show()

    app.exec()
