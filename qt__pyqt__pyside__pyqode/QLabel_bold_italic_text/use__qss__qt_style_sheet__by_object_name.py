#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QLabel, QVBoxLayout, QWidget


app = QApplication([])
app.setStyleSheet(
    """
#welcome { font: bold italic }
#label_foo_bar { 
    font: italic;
    color: green;
}
"""
)

label_1 = QLabel()
label_1.setObjectName("welcome")
label_1.setText("Hello World!!!")

label_2 = QLabel()
label_2.setText("nothing...")

label_3 = QLabel()
label_3.setObjectName("label_foo_bar")
label_3.setText("FooBar")

layout = QVBoxLayout()
layout.addWidget(label_1)
layout.addWidget(label_2)
layout.addWidget(label_3)

mw = QWidget()
mw.setLayout(layout)
mw.show()

app.exec()
