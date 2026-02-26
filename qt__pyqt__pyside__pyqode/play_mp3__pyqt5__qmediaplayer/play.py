#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


def _on_media_status_changed(status) -> None:
    if status == Qt.QMediaPlayer.EndOfMedia:
        Qt.QCoreApplication.instance().quit()


app = Qt.QCoreApplication([])

player = Qt.QMediaPlayer()
file_name = Qt.QUrl.fromLocalFile("example.mp3")
player.setMedia(Qt.QMediaContent(file_name))
player.mediaStatusChanged.connect(_on_media_status_changed)
player.play()

app.exec()
