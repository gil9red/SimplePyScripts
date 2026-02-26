#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication, QMainWindow
from PyQt5.QtGui import QPaintEvent, QPainter, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer


# SOURCE: https://ru.stackoverflow.com/a/860257/201445
class WelcomeWidget(QDialog):
    def __init__(self, text="Welcome my app", duration=3000) -> None:
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        label = QLabel(text)
        label.setStyleSheet(
            """
            color : #fff;
            margin-top: 6px;
            margin-bottom: 6px;
            margin-left: 10px;
            margin-right: 10px;
            font-size: 50px;
        """
        )
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        self.timer = QTimer()
        self.timer.setInterval(duration)
        self.timer.timeout.connect(self.close)

    def exec(self) -> None:
        self.timer.start()
        self.animation.start()

        super().exec()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0, 180))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)


if __name__ == "__main__":
    app = QApplication([])

    WelcomeWidget().exec()
    WelcomeWidget("Еще, раз! Привет!", duration=1500).exec()

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()

            self.setWindowTitle("MAIN WINDOW")
            self.setFixedSize(500, 500)

            label = QLabel("MAIN WINDOW")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 50px;")
            self.setCentralWidget(label)

    mw = MainWindow()
    mw.show()

    app.exec()
