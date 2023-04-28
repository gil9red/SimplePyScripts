#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Bridge — Мост
# SOURCE: https://ru.wikipedia.org/wiki/Мост_(шаблон_проектирования)


from abc import ABC, abstractmethod


class Drawer(ABC):
    @abstractmethod
    def draw_circle(self, x: int, y: int, radius: int):
        pass


class SmallCircleDrawer(Drawer):
    RADIUS_MULTIPLIER = 0.25

    def draw_circle(self, x: int, y: int, radius: int):
        print(
            f"Small circle center = {x},{y} radius = {radius * self.RADIUS_MULTIPLIER}"
        )


class LargeCircleDrawer(Drawer):
    RADIUS_MULTIPLIER = 10

    def draw_circle(self, x: int, y: int, radius: int):
        print(
            f"Large circle center = {x},{y} radius = {radius * self.RADIUS_MULTIPLIER}"
        )


class Shape(ABC):
    def __init__(self, drawer: Drawer):
        self._drawer = drawer

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def enlarge_radius(self, multiplier: int):
        pass


class Circle(Shape):
    def __init__(self, x: int, y: int, radius: int, drawer: Drawer):
        super().__init__(drawer)

        self._x = x
        self._y = y
        self._radius = radius

    def draw(self):
        self._drawer.draw_circle(self._x, self._y, self._radius)

    def enlarge_radius(self, multiplier: int):
        self._radius *= multiplier

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_radius(self) -> int:
        return self._radius

    def set_x(self, x: int):
        self._x = x

    def set_y(self, y: int):
        self._y = y

    def set_radius(self, radius: int):
        self._radius = radius


if __name__ == "__main__":
    shapes = [
        Circle(5, 10, 10, LargeCircleDrawer()),
        Circle(20, 30, 100, SmallCircleDrawer()),
    ]
    for x in shapes:
        x.draw()

    # Output
    # Large circle center = 5,10 radius = 100
    # Small circle center = 20,30 radius = 25.0
