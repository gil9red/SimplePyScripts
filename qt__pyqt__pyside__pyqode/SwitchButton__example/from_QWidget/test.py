#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from switch_button import SwitchButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        switch_btn1 = SwitchButton(self, "On", 15, "Off", 31, width=60)
        label_switch_btn1 = QLabel(
            f"Checked: {switch_btn1.isChecked()}, text: {switch_btn1.valueText()}"
        )
        switch_btn1.clicked.connect(
            lambda checked: label_switch_btn1.setText(
                f"Checked: {switch_btn1.isChecked()}, text: {switch_btn1.valueText()}"
            )
        )

        switch_btn2 = SwitchButton(self, "Вкл", 15, "Откл", 31, width=120)
        label_switch_btn2 = QLabel(
            f"Checked: {switch_btn2.isChecked()}, text: {switch_btn2.valueText()}"
        )
        switch_btn2.clicked.connect(
            lambda checked: label_switch_btn2.setText(
                f"Checked: {switch_btn2.isChecked()}, text: {switch_btn2.valueText()}"
            )
        )

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(switch_btn1)
        main_layout.addWidget(label_switch_btn1)

        main_layout.addWidget(switch_btn2)
        main_layout.addWidget(label_switch_btn2)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
