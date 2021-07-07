#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

from PyQt5.QtGui import QGuiApplication, QPainter, QImage, QPen
from PyQt5.QtCore import Qt

from time_intervals__call_center import Interval, find_max_intersection


items = [
    Interval(DT.datetime(2021, 4, 21, 12, 0, 0),  20 * 60),
    Interval(DT.datetime(2021, 4, 21, 12, 10, 0), 10 * 60),
    Interval(DT.datetime(2021, 4, 21, 12, 15, 0), 30 * 60),
    Interval(DT.datetime(2021, 4, 21, 13, 0, 0),  30 * 60),
]
items.sort(key=lambda x: x.start)
print(find_max_intersection(items))

start_time = items[0].start

app = QGuiApplication([])

img = QImage(600, 100, QImage.Format_RGB32)
img.fill(Qt.black)

painter = QPainter(img)
painter.setPen(QPen(Qt.white, 2))

multiplicity = 10
y = 10
for interval in items:
    seconds = (interval.start - start_time).total_seconds()
    duration_seconds = (interval.end - interval.start).total_seconds()
    # print(interval, seconds, duration_seconds)

    x1 = 10 + seconds / multiplicity
    x2 = x1 + duration_seconds / multiplicity
    # print(f'{x1}x{y} {x2}x{y}')
    painter.drawLine(x1, y, x2, y)

    y += 10

img.save(__file__ + '.png')

