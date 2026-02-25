#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/Заместитель_(шаблон_проектирования)


from abc import ABC, abstractmethod


class IMath(ABC):
    """Интерфейс для прокси и реального субъекта"""

    @abstractmethod
    def add(self, x, y):
        raise NotImplementedError()

    @abstractmethod
    def sub(self, x, y):
        raise NotImplementedError()

    @abstractmethod
    def mul(self, x, y):
        raise NotImplementedError()

    @abstractmethod
    def div(self, x, y):
        raise NotImplementedError()


class Math(IMath):
    """Реальный субъект"""

    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    def mul(self, x, y):
        return x * y

    def div(self, x, y):
        return x / y


class MathProxy(IMath):
    """Прокси"""

    def __init__(self) -> None:
        self.math = None

    # Быстрые операции - не требуют реального субъекта
    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    # Медленная операция - требует создания реального субъекта
    def mul(self, x, y):
        if not self.math:
            self.math = Math()

        return self.math.mul(x, y)

    def div(self, x, y):
        if y == 0:
            return float("inf")  # Вернуть positive infinity

        if not self.math:
            self.math = Math()

        return self.math.div(x, y)


if __name__ == "__main__":
    p = MathProxy()
    x, y = 4, 2
    print("4 + 2 =", p.add(x, y))
    print("4 - 2 =", p.sub(x, y))
    print("4 * 2 =", p.mul(x, y))
    print("4 / 2 =", p.div(x, y))
