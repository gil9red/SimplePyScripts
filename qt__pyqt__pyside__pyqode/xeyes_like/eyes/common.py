#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from math import fabs, sqrt

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QWidget


MINIMAL_WIDTH_EYE: int = 50
MINIMAL_HEIGHT_EYE: int = 50

MAXIMAL_WIDTH_EYE: int = 350
MAXIMAL_HEIGHT_EYE: int = 350

EPS: float = 0.00001


@dataclass
class Ellipse:
    x1: float = 0.0
    y1: float = 0.0
    rx: float = 0.0
    ry: float = 0.0


@dataclass
class Line:
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0


class ResultCrossLineAndEllipse:
    x1: float = 0
    y1: float = 0
    x2: float = 0
    y2: float = 0


def is_ellipse_and_direct(
    ellipse: Ellipse,
    line: Line,
    result: ResultCrossLineAndEllipse,
) -> bool:
    """
    Функция, которая считает пересечения эллипса и прямой
    Когда пересечений нет, возвращает False, иначе True, а
    в result присваивается точка пересечения

    :param ellipse:
    :param line:
    :param result:
    :return:
    """

    dx: float = line.x1 - line.x2

    # Если какой-то радиус равен 0
    if fabs(ellipse.rx) < EPS or fabs(ellipse.ry) < EPS:
        if (
            fabs(ellipse.rx) < EPS
            and fabs(line.x1 - ellipse.x1) < EPS
            and fabs(line.x2 - ellipse.x1) < EPS
        ):
            result.x1 = ellipse.x1
            result.y1 = ellipse.y1 - ellipse.ry
            result.x2 = ellipse.x1
            result.y2 = ellipse.y1 + ellipse.ry
            return True

        if (
            fabs(ellipse.ry) < EPS
            and fabs(line.y1 - ellipse.y1) < EPS
            and fabs(line.y2 - ellipse.y1) < EPS
        ):
            result.x1 = ellipse.x1 - ellipse.rx
            result.y1 = ellipse.y1
            result.x2 = ellipse.x1 + ellipse.rx
            result.y2 = ellipse.y1
            return True

    if fabs(dx) < EPS:
        # Вертикальная прямая
        nx: float = line.x1 - ellipse.x1

        # Пересечения нет
        if nx < -ellipse.rx or ellipse.rx < nx or fabs(ellipse.rx) < EPS:
            return False

        result.x1 = nx
        result.y1 = sqrt(
            ellipse.ry * ellipse.ry * (1 - nx * nx / (ellipse.rx * ellipse.rx))
        )
        result.x2 = nx
        result.y2 = -result.y1

    else:
        dy: float = line.y1 - line.y2

        # lnk и lnb - коэффициенты прямой по формуле lnk * x + lnb  ==  y
        lnk: float = dy / dx
        lnb: float = (
            ellipse.x1 * dy
            + line.x1 * line.y2
            - line.y1 * line.x2
            - ellipse.y1 * dx
        ) / dx

        # Получаем уравнение пересечения: a0 x^2 + a1 x + a2  ==  0
        a0: float = lnk * lnk + ellipse.ry * ellipse.ry / (ellipse.rx * ellipse.rx)
        a1: float = 2 * lnb * lnk
        a2: float = lnb * lnb - ellipse.ry * ellipse.ry

        # Решения квадратного уравнения a0 x^2 + a1 x + a2 == 0
        # Это и будет координаты X пересечений
        disc: float = a1 * a1 - 4 * a0 * a2

        # Пересечения нет
        if disc < 0 or fabs(a0) < EPS:
            return False

        result.x1 = (-a1 - sqrt(disc)) / (2 * a0)
        result.y1 = lnk * result.x1 + lnb
        result.x2 = (-a1 + sqrt(disc)) / (2 * a0)
        result.y2 = lnk * result.x2 + lnb

    result.x1 += ellipse.x1
    result.y1 += ellipse.y1
    result.x2 += ellipse.x1
    result.y2 += ellipse.y1

    return True


def percent_number(number: float, percent: int) -> float:
    return number if percent < 0 else (number / 100) * percent


def set_top_of_all_windows(widget: QWidget, top: bool):
    old_pos: QPoint = widget.pos()

    if top:
        flags = Qt.Tool | Qt.WindowStaysOnTopHint
    else:
        flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint

    widget.setWindowFlags(flags)

    widget.showNormal()
    widget.move(old_pos)
