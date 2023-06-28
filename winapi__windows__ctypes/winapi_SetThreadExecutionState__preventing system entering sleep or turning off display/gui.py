#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import QtWidgets as qtw
from main import preventing_on, preventing_off


if __name__ == "__main__":
    app = qtw.QApplication([])

    w = qtw.QWidget()
    w.setWindowTitle("Preventing entering sleep or turning off the display")
    w.setLayout(qtw.QVBoxLayout())

    def button_clicked(checked):
        if checked:
            button.setText("On")
            preventing_on()
        else:
            button.setText("Off")
            preventing_off()

    button = qtw.QPushButton()
    button.toggled.connect(button_clicked)
    button.setCheckable(True)
    button.setChecked(True)

    font = button.font()
    font.setPointSize(20)

    button.setFont(font)
    button.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

    w.layout().addWidget(qtw.QLabel(w.windowTitle()))
    w.layout().addWidget(button)
    w.show()

    app.exec()
