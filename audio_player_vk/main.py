#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Simple audio player vk.com"""


import sys
import traceback

from PyQt5.QtWidgets import *

from auth_page import AuthPage
from audio_player_page import AudioPlayerPage

from common import log


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    log.critical(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncaught_exceptions


TITLE = 'audio_player_vk'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.update_title()

        self.auth_page = AuthPage()
        self.auth_page.about_successful_auth.connect(self.go_audio_player_page)

        self.audio_player_page = AudioPlayerPage()
        self.audio_player_page.about_play_audio.connect(self.update_title)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.auth_page)
        self.stacked_widget.addWidget(self.audio_player_page)

        self.setCentralWidget(self.stacked_widget)

    def update_title(self, audio_title=''):
        self.setWindowTitle(TITLE + '. ' + audio_title)

    def go_audio_player_page(self):
        self.stacked_widget.setCurrentWidget(self.audio_player_page)

        vk = self.auth_page.vk
        self.audio_player_page.fill(vk)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
