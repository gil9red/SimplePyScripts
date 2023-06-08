#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import sqlite3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


if __name__ == "__main__":
    con = sqlite3.connect("test.sqlite")
    cur = con.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS Images (
        Data BLOB
    )
    """
    )
    con.commit()

    with open("capture.png", mode="rb") as f:
        binary = sqlite3.Binary(f.read())

        cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,))
        con.commit()

    app = QApplication([])

    w = QWidget()
    layout = QVBoxLayout()
    w.setLayout(layout)

    for (img_data,) in con.execute("SELECT Data from Images"):
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)

        label = QLabel()
        label.setPixmap(pixmap)

        layout.addWidget(label)

    w.show()

    sys.exit(app.exec_())
