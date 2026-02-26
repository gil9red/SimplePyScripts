#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

import cv2

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap


class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, source) -> None:
        super().__init__()

        self.source = source

    def run(self) -> None:
        # SOURCE: https://stackoverflow.com/a/44404713/5909792
        cap = cv2.VideoCapture(self.source)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888
                )
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

                cv2.waitKey(28)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.label_video = QLabel()
        self.label_video.setMinimumSize(600, 480)

        self.pb_play = QPushButton("Play")
        self.pb_play.clicked.connect(self.playVideo)

        self.thread = ThreadOpenCV("video.mp4")
        self.thread.changePixmap.connect(self.setImage)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_video)
        main_layout.addWidget(self.pb_play)

        self.setLayout(main_layout)

    def playVideo(self) -> None:
        self.thread.start()

    def setImage(self, image) -> None:
        self.label_video.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = Widget()
    mw.show()

    sys.exit(app.exec_())
