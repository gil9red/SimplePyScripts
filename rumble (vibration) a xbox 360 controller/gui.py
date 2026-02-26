#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from rumble import set_vibration


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Rumble (vibration) a xbox 360 controller")

        self.button_vibration = QPushButton("Rumble / Vibration")
        self.button_vibration.setCheckable(True)
        self.button_vibration.clicked.connect(self._enable_vibration)

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._timeout)

        self.left_motor = QSlider(Qt.Horizontal)
        self.left_motor.setRange(0, 65535)

        label_left_motor = QLabel(str(self.left_motor.value()))
        label_left_motor.setAlignment(Qt.AlignCenter)
        self.left_motor.valueChanged.connect(
            lambda x: label_left_motor.setText(str(x))
        )

        self.right_motor = QSlider(Qt.Horizontal)
        self.right_motor.setRange(0, 65535)
        self.right_motor.setValue(32767)

        label_right_motor = QLabel(str(self.right_motor.value()))
        label_right_motor.setAlignment(Qt.AlignCenter)
        self.right_motor.valueChanged.connect(
            lambda x: label_right_motor.setText(str(x))
        )

        layout_left_motor = QVBoxLayout()
        layout_right_motor = QVBoxLayout()

        layout_left_motor.addWidget(QLabel("Left motor:"))
        layout_left_motor.addWidget(self.left_motor)
        layout_left_motor.addWidget(label_left_motor)
        layout_left_motor.addStretch()

        layout_right_motor.addWidget(QLabel("Right motor:"))
        layout_right_motor.addWidget(self.right_motor)
        layout_right_motor.addWidget(label_right_motor)
        layout_right_motor.addStretch()

        layout_motors = QHBoxLayout()
        layout_motors.addLayout(layout_left_motor)
        layout_motors.addLayout(layout_right_motor)

        layout = QVBoxLayout()
        layout.addWidget(self.button_vibration)
        layout.addLayout(layout_motors)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _enable_vibration(self, enable) -> None:
        if enable:
            self.timer.start()
        else:
            self.timer.stop()
            set_vibration(0, 0)

    def _timeout(self) -> None:
        set_vibration(self.left_motor.value(), self.right_motor.value())


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
