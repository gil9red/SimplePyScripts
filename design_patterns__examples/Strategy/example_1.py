#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Strategy — Стратегия
# SOURCE: https://ru.wikipedia.org/wiki/Стратегия_(шаблон_проектирования)


from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def action(self, a, b):
        pass


class AdditionStrategy(Strategy):
    def action(self, a, b):
        return a + b


class SubtractionStrategy(Strategy):
    def action(self, a, b):
        return a - b


class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def action(self, a, b):
        return self._strategy.action(a, b)


if __name__ == "__main__":
    context = Context(AdditionStrategy())
    print(context.action(10, 5))  # 15
    print()

    context = Context(SubtractionStrategy())
    print(context.action(10, 5))  # 5

    context.set_strategy(AdditionStrategy())
    print(context.action(10, 5))  # 15
