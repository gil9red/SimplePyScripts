#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtGui import QGuiApplication, QPixmap
from PyQt5.QtCore import Qt


app = QGuiApplication([])

pixmap = QPixmap("cat.jpg")
pixmap.setMask(pixmap.createHeuristicMask(Qt.transparent))
pixmap.save('cat.png')
