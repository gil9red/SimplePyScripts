#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from math import fabs, sqrt


# TODO: upper
eps: float = 0.00001


# TODO: rename
@dataclass
class UEllipse:
    x1: float = 0.0
    y1: float = 0.0
    rx: float = 0.0
    ry: float = 0.0


# TODO: rename
@dataclass
class ULine:
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0


# TODO: rename
class UResultCrossLineAndEllipse:
    x1: float = 0
    y1: float = 0
    x2: float = 0
    y2: float = 0


# TODO: rename
class UIntersection:
    # Функция, которая считает пересечения эллипса и прямой
    # Когда пересечений нет, возвращает False, иначе True, а
    # в result присваивается точка пересечения
    @staticmethod
    def isEllipseAndDirect(
        ellipse: UEllipse, line: ULine, result: UResultCrossLineAndEllipse
    ) -> bool:
        dx: float = line.x1 - line.x2

        # Если какой-то радиус равен 0
        if fabs(ellipse.rx) < eps or fabs(ellipse.ry) < eps:
            if (
                fabs(ellipse.rx) < eps
                and fabs(line.x1 - ellipse.x1) < eps
                and fabs(line.x2 - ellipse.x1) < eps
            ):
                result.x1 = ellipse.x1
                result.y1 = ellipse.y1 - ellipse.ry
                result.x2 = ellipse.x1
                result.y2 = ellipse.y1 + ellipse.ry
                return True

            if (
                fabs(ellipse.ry) < eps
                and fabs(line.y1 - ellipse.y1) < eps
                and fabs(line.y2 - ellipse.y1) < eps
            ):
                result.x1 = ellipse.x1 - ellipse.rx
                result.y1 = ellipse.y1
                result.x2 = ellipse.x1 + ellipse.rx
                result.y2 = ellipse.y1
                return True

        if fabs(dx) < eps:
            # Вертикальная прямая
            nx: float = line.x1 - ellipse.x1

            # Пересечения нет
            if nx < -ellipse.rx or ellipse.rx < nx or fabs(ellipse.rx) < eps:
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
            if disc < 0 or fabs(a0) < eps:
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


# TODO: rename
class USupport:
    # Процент от числа
    @staticmethod
    def percentNumber(number: float, percent: int) -> float:
        return number if percent < 0 else (number / 100) * percent


# TODO: rename
minimalWidthEye: int = 50
minimalHeightEye: int = 50

maximalWidthEye: int = 350
maximalHeightEye: int = 350
