#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import functools
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor


CELL_SIZE: int = 20


def painter_context(func: Callable):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        painter: QPainter | None = None
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, QPainter):
                painter = arg
                break

        if painter:
            painter.save()
        try:
            return func(*args, **kwargs)
        finally:
            if painter:
                painter.restore()

    return decorated


def draw_cell_board(
    painter: QPainter,
    x: int,
    y: int,
    color: QColor,
    pen: Qt.GlobalColor = Qt.NoPen,
    cell_size: int = CELL_SIZE,
    indent: int = 0,
):
    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(
        (x * cell_size) + indent,
        (y * cell_size) + indent,
        cell_size,
        cell_size,
    )


class StatusGameEnum(enum.IntEnum):
    INITED = enum.auto()
    STARTED = enum.auto()
    PAUSED = enum.auto()
    FINISHED = enum.auto()
