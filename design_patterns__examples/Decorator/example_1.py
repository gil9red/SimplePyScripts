#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Decorator — Декоратор
# SOURCE: https://ru.wikipedia.org/wiki/Декоратор_(шаблон_проектирования)


from abc import ABC, abstractmethod


class IOperation(ABC):
    @abstractmethod
    def run(self, text: str) -> str:
        pass


class SimpleOperation(IOperation):
    def run(self, text: str) -> str:
        return text


class BaseDecorator(IOperation):
    def __init__(self, operation: IOperation) -> None:
        self._wrapped = operation


class BoldDecorator(BaseDecorator):
    def run(self, text: str) -> str:
        return "<b>" + self._wrapped.run(text) + "</b>"


class ItalicDecorator(BaseDecorator):
    def run(self, text: str) -> str:
        return "<i>" + self._wrapped.run(text) + "</i>"


class UpperDecorator(BaseDecorator):
    def run(self, text: str) -> str:
        return self._wrapped.run(text).upper()


if __name__ == "__main__":
    text = "Hello World!"

    operation = SimpleOperation()
    print(operation.run(text))  # Hello World!

    operation = BoldDecorator(operation)
    print(operation.run(text))  # <b>Hello World!</b>

    operation = ItalicDecorator(operation)
    print(operation.run(text))  # <i><b>Hello World!</b></i>

    operation = UpperDecorator(operation)
    print(operation.run(text))  # <I><B>HELLO WORLD!</B></I>
    print()

    # ItalicDecorator -> BoldDecorator -> UpperDecorator -> SimpleOperation
    operation = SimpleOperation()
    operation = UpperDecorator(operation)
    operation = BoldDecorator(operation)
    operation = ItalicDecorator(operation)
    print(operation.run(text))  # <i><b>HELLO WORLD!</b></i>
    print()

    # ItalicDecorator -> BoldDecorator -> UpperDecorator -> SimpleOperation
    operation = ItalicDecorator(BoldDecorator(UpperDecorator(SimpleOperation())))
    print(operation.run(text))  # <i><b>HELLO WORLD!</b></i>
