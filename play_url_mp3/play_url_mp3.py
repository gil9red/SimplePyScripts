#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys

from urllib.request import urlretrieve
from urllib.parse import urlparse

from PySide.QtGui import *
from PySide.phonon import Phonon


if __name__ == "__main__":
    app = QApplication(sys.argv)

    audio = Phonon.MediaObject()
    audio.setCurrentSource(Phonon.MediaSource(""))
    output = Phonon.AudioOutput(Phonon.MusicCategory)
    Phonon.createPath(audio, output)

    widget = QWidget()
    widget.setWindowTitle("Simple url audio player")

    line_edit_url = QLineEdit()
    line_edit_url.setText(
        "https://www.dropbox.com/sh/a4bwzhn0s584u73/AACgDRii1rtCmoL3mXEwlXDga/CallYourName.mp3?dl=1"
    )

    def play():
        url = line_edit_url.text()

        # Выдираем из url имя файла
        file_name = os.path.split(urlparse(url).path)[-1]
        if not os.path.exists(file_name):
            urlretrieve(url, file_name)

        audio.setCurrentSource(Phonon.MediaSource(file_name))
        audio.play()

    play_url = QPushButton("Play")
    play_url.clicked.connect(play)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Url audio:"))
    layout.addWidget(line_edit_url)
    layout.addWidget(play_url)

    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec_())
