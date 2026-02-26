#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QGroupBox, QCheckBox, QButtonGroup, QGridLayout


def _on_button_clicked(button: QCheckBox) -> None:
    print(button, button.text(), button.isChecked())


app = QApplication([])

button_group = QButtonGroup()
button_group.setExclusive(False)
button_group.buttonClicked.connect(_on_button_clicked)

buttons_array = [
    [QCheckBox("a1"), QCheckBox("a2"), QCheckBox("a3")],
    [QCheckBox("b1"), QCheckBox("b2"), QCheckBox("b3")],
    [QCheckBox("c1"), QCheckBox("c2"), QCheckBox("c3")],
]

main_layout = QGridLayout()

for i, row in enumerate(buttons_array):
    for j, button in enumerate(row):
        button_group.addButton(button)
        main_layout.addWidget(button, i, j)

mw = QGroupBox()
mw.setLayout(main_layout)
mw.show()

app.exec()
