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


import time


class CheckJobReportThread(QThread):
    about_new_text = Signal(str)
    about_ok = Signal(bool)

    def __init__(self):
        super().__init__()

        self.last_text = None
        self.ok = None

    def run(self):
        while True:
            today = datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            print('Check for', today)

            name, deviation_hours = get_user_and_deviation_hours()

            ok = deviation_hours[0] != '-'
            text = name + '\n' + ('Переработка' if ok else 'Недоработка') + ' ' + deviation_hours

            if self.last_text != text:
                print('    ' + text.strip().replace('\n', ' ') + '\n')
                self.last_text = text

                text = 'Обновлено {}\n{}'.format(today, self.last_text)
                self.about_new_text.emit(text)

            if self.ok != ok:
                self.ok = ok
                self.about_ok.emit(self.ok)

            time.sleep(3600)


class JobReportWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.info = QLabel()
        self.ok = None

        self.quit_button = QToolButton()
        self.quit_button.setText('Quit')
        self.quit_button.setAutoRaise(True)
        self.quit_button.clicked.connect(QApplication.instance().quit)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.info)
        layout.addStretch()
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

        self.thread = CheckJobReportThread()
        self.thread.about_new_text.connect(self.info.setText)
        self.thread.about_ok.connect(self._set_ok)
        self.thread.start()

    def _set_ok(self, val):
        self.ok = val
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        color = QColor('#29AB87') if self.ok else QColor(255, 0, 0, 128)

        painter = QPainter(self)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QApplication([])

    tray = QSystemTrayIcon(QIcon(TRAY_ICON))

    job_report_widget = JobReportWidget()
    job_report_widget.setFixedSize(200, 100)
    job_report_widget_action = QWidgetAction(job_report_widget)
    job_report_widget_action.setDefaultWidget(job_report_widget)

    menu = QMenu()
    menu.addAction(job_report_widget_action)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda x: menu.exec(tray.geometry().center()))

    tray.setToolTip('Compass Plus. Рапорт учета рабочего времени')
    tray.show()

    app.exec()
