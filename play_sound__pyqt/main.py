#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from multiprocessing import Process

from PyQt5.QtCore import QCoreApplication, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer


def play(file_name: str):
    if not os.path.exists(file_name):
        raise FileNotFoundError(file_name)

    app = QCoreApplication([])

    url = QUrl.fromLocalFile(file_name)

    playlist = QMediaPlaylist()
    playlist.addMedia(QMediaContent(url))

    player = QMediaPlayer()
    player.setPlaylist(playlist)
    player.play()

    def tick():
        if player.state() == QMediaPlayer.StoppedState:
            app.quit()

    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(1000)

    app.exec()


def play_async(file_name: str):
    # from threading import Thread
    # thread = Thread(target=play, args=(file_name,))
    # thread.start()

    process = Process(target=play, args=(file_name,))
    process.start()


if __name__ == "__main__":
    file_name = r"..\speak\play_mp3\speak_male.mp3"
    play(file_name)

    import time

    play_async(file_name)
    time.sleep(0.2)

    play_async(file_name)
    time.sleep(0.2)

    play_async(file_name)
