#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PySide.QtCore import QCoreApplication, QEventLoop
from PySide.phonon import Phonon


try:
    app = QCoreApplication(sys.argv)
except RuntimeError:
    app = QCoreApplication.instance()


audio = Phonon.MediaObject()
output = Phonon.AudioOutput(Phonon.MusicCategory)
Phonon.createPath(audio, output)


def play(file_name):
    audio.setCurrentSource(Phonon.MediaSource(file_name))
    audio.play()

    loop = QEventLoop()
    audio.finished.connect(loop.quit)
    loop.exec_()
