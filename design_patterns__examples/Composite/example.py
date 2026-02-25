#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Composite - Компоновщик
# SOURCE: https://ru.wikipedia.org/wiki/Компоновщик_(шаблон_проектирования)


from abc import ABC, abstractmethod
from typing import List


class Graphic(ABC):
    @abstractmethod
    def draw(self, *args, **kwargs):
        pass


class CompositeGraphic(Graphic):
    def __init__(self) -> None:
        self._child_graphics: List[Graphic] = []

    def draw(self, *args, **kwargs) -> None:
        for graphic in self._child_graphics:
            graphic.draw(*args, **kwargs)

    # Adds the graphic to the composition
    def add(self, graphic: Graphic) -> None:
        if graphic in self._child_graphics:
            return

        self._child_graphics.append(graphic)

    # Removes the graphic from the composition
    def remove(self, graphic: Graphic) -> None:
        self._child_graphics.remove(graphic)


class Ellipse(Graphic):
    def __init__(self, x, y, rx, ry) -> None:
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry

    def draw(self, *args, **kwargs) -> None:
        print(f"Ellipse: x={self.x}, y={self.y}, rx={self.rx}, ry={self.ry}")


class Point(Graphic):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self, *args, **kwargs) -> None:
        print(f"Point: x={self.x}, y={self.y}")


class Rect(Graphic):
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, *args, **kwargs) -> None:
        print(f"Rect: x={self.x}, y={self.y}, w={self.w}, h={self.h}")


class Line(Graphic):
    def __init__(self, x1, y1, x2, y2) -> None:
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

    def draw(self, *args, **kwargs) -> None:
        print(f"Line: x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2}")


if __name__ == "__main__":
    ellipse_1 = Ellipse(x=50, y=50, rx=10, ry=15)
    ellipse_2 = Ellipse(x=10, y=5, rx=40, ry=50)

    composite_1 = CompositeGraphic()
    composite_1.add(ellipse_1)
    composite_1.add(Point(4, 4))
    composite_1.add(Point(4, 5))
    composite_1.add(Point(4, 6))

    composite_main = CompositeGraphic()
    composite_main.add(ellipse_2)
    composite_main.add(Rect(30, 20, 50, 30))
    composite_main.add(Rect(100, 70, 50, 50))
    composite_main.add(composite_1)
    composite_main.add(Line(60, 10, 25, 25))

    composite_main.draw()
