#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import Qt


img = QImage(r'video-game-192x192.png')
img2 = QImage(img.size(), QImage.Format_ARGB32)
img2.fill(Qt.transparent)

p = QPainter(img2)
p.setOpacity(0.85)
p.drawImage(img.rect(), img)

img2.save(r'video-game-192x192__transparent.png')
