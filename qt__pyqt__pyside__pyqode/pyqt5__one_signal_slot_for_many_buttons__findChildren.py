#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QGroupBox, QCheckBox, QGridLayout, QObject


def _on_button_clicked(checked: bool):
    # Небольшой костыль для получения объекта, который отправил сигнал
    # Костыль не нужен будет если метод будет внутри виджета -- button = self.sender()
    button = QObject().sender()
    print(button, button.text(), button.isChecked(), checked)


app = QApplication([])

buttons_array = [
    [QCheckBox("a1"), QCheckBox("a2"), QCheckBox("a3")],
    [QCheckBox("b1"), QCheckBox("b2"), QCheckBox("b3")],
    [QCheckBox("c1"), QCheckBox("c2"), QCheckBox("c3")],
]

main_layout = QGridLayout()

for i, row in enumerate(buttons_array):
    for j, button in enumerate(row):
        main_layout.addWidget(button, i, j)

mw = QGroupBox()
mw.setLayout(main_layout)

# Ищем у QGroupBox наши кнопки, чтобы им указать сигнал
for button in mw.findChildren(QCheckBox):
    button.clicked.connect(_on_button_clicked)

mw.show()

app.exec()
