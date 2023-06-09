#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QWidget, QVBoxLayout, QComboBox


app = QApplication([])

combo_box = QComboBox()

for i in range(10):
    combo_box.addItem("item_" + str(i + 1))

# QStandardItemModel, метод model.item возвращает объекты QStandardItem
model = combo_box.model()

# Указываем какие элементы сделать невыбираемыми
model.item(0).setEnabled(False)
model.item(2).setEnabled(False)
model.item(4).setEnabled(False)

combo_box.setCurrentIndex(-1)

layout = QVBoxLayout()
layout.addWidget(combo_box)

mw = QWidget()
mw.setLayout(layout)
mw.show()

app.exec()
