#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Flyweight — Приспособленец
# SOURCE: https://ru.wikipedia.org/wiki/Приспособленец_(шаблон_проектирования)


# SOURCE: https://javarush.ru/groups/posts/584-patternih-proektirovanija


class Flyweight:
    def __init__(self, row: int):
        self.row = row
        print("ctor:", self.row)

    def report(self, col: int):
        print(f" {self.row}{col}", end="")


class Factory:
    def __init__(self, max_rows: int):
        self._pool: list[Flyweight | None] = [None] * max_rows

    def get_flyweight(self, row: int) -> Flyweight:
        if self._pool[row] is None:
            self._pool[row] = Flyweight(row)

        return self._pool[row]


if __name__ == "__main__":
    rows = 5
    the_factory = Factory(rows)
    for i in range(rows):
        for j in range(rows):
            the_factory.get_flyweight(i).report(j)

        print()
