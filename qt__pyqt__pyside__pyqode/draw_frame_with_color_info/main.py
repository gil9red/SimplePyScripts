#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Union
import sys

sys.path.append('..')

from Good_text_foreground_color_for_a_given_background_color import get_good_text_foreground_color

from PyQt5.QtGui import QGuiApplication, QPainter, QImage, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice


APP = QGuiApplication([])
SIZE = 300
RADIUS = 20
FAMILY_FONT = 'Courier New'  # Need monospaced


def get_optimal_font(family_font: str, w, h, text: str) -> QFont:
    font = QFont(family_font)
    font.setStyleHint(QFont.Courier, QFont.PreferAntialias)
    metrics = QFontMetrics(font)

    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/add91e36e1ee59b3956b9fafdcffc9f4ff10ed3d/qt__pyqt__pyside__pyqode/pyqt__QPainter__draw_table.py#L98
    factor = w / metrics.boundingRect(0, 0, w, h, Qt.AlignCenter, text).width()
    if factor < 1 or factor > 1.25:
        font.setPointSizeF(font.pointSizeF() * factor)

    return font


def draw_hex(painter: QPainter, size: int, color: QColor):
    r, g, b, _ = color.getRgb()
    value = ''.join(f'{x:02X}' for x in [r, g, b])

    text_color = get_good_text_foreground_color(color)

    x, y, w_hex, h_hex = size * 0.05, size * 0.1, size * 0.9, size * 0.25
    font = get_optimal_font(FAMILY_FONT, w_hex, h_hex, text='FFFFFF')

    painter.save()

    painter.setPen(text_color)
    painter.setFont(font)

    painter.drawText(x, y, w_hex, h_hex, Qt.AlignCenter, value)

    painter.restore()


def draw_rgb(painter: QPainter, size: int, color: QColor):
    r, g, b, _ = color.getRgb()
    rgb = list(map(str, [r, g, b]))

    text_color, back_color = Qt.black, Qt.white

    w_rgb, h_rgb = size // 4, size // 6
    font = get_optimal_font(FAMILY_FONT, w_rgb, h_rgb, text='255')
    font.setWeight(QFont.Bold)

    y = size - size // 4
    indent = (size * 0.25) // 4
    radius = 30

    for i, value in enumerate(rgb):
        x = indent + indent * i + w_rgb * i

        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(back_color)
        painter.drawRoundedRect(x, y, w_rgb, h_rgb, radius, radius, Qt.RelativeSize)
        painter.restore()

        painter.save()
        painter.setPen(text_color)
        painter.setFont(font)
        painter.drawText(x, y, w_rgb, h_rgb, Qt.AlignCenter, value)
        painter.restore()


def get_frame_color_info(color: QColor, size=SIZE, rounded=True, as_bytes=False) -> Union[QImage, bytes]:
    image = QImage(size, size, QImage.Format_ARGB32)
    image.fill(Qt.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(color)

    if rounded:
        painter.drawRoundedRect(0, 0, image.width(), image.height(), RADIUS, RADIUS, Qt.RelativeSize)
    else:
        painter.drawRect(0, 0, image.width(), image.height())

    draw_hex(painter, size, color)
    draw_rgb(painter, size, color)

    painter.end()

    if as_bytes:
        ba = QByteArray()
        buff = QBuffer(ba)
        buff.open(QIODevice.WriteOnly)
        image.save(buff, "PNG")
        return ba.data()

    return image


if __name__ == '__main__':
    for name in ['#007396', '#ff8c69', 'green', '#a000ff00']:
        color = QColor(name)
        image = get_frame_color_info(color)
        image.save(f'images/{name}.png')

    name = '#007396'
    image = get_frame_color_info(QColor(name), rounded=False)
    image.save(f'images/no_rounded_{name}.png')
