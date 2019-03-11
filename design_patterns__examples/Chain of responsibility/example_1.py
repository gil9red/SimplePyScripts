#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: Design Patterns: Chain of responsibility — Цепочка обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей


from abc import ABC, abstractmethod
import re


class Handler(ABC):
    """
    Базовый класс обработчика объявляет метод построения цепочки обработчиков.
    Он также объявляет метод для обработки.
    """

    _next_handler: 'Handler' = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return self._next_handler

    @abstractmethod
    def handle(self, obj):
        # Вызываем следующий обработки
        if self._next_handler:
            self._next_handler.handle(obj)


class IsNotNoneHandler(Handler):
    def handle(self, obj):
        if obj is None:
            raise Exception(f"Object is None!")

        return super().handle(obj)


class IsStringHandler(Handler):
    def handle(self, obj):
        if type(obj) != str:
            raise Exception(f"Object {repr(obj)} is not string!")

        return super().handle(obj)


class IsMatchReHandler(Handler):
    def __init__(self, re_pattern: str):
        self._re_pattern = re_pattern

    def handle(self, obj):
        if not re.search(self._re_pattern, obj):
            raise Exception(f'String {repr(obj)} is not matching by regexp: "{self._re_pattern}"!')

        return super().handle(obj)


if __name__ == '__main__':
    def client_code(handler: Handler):
        for obj in [None, '123', '456', '111', 456]:
            try:
                handler.handle(obj)
                print(f'Object {repr(obj)} ok!')

            except Exception as e:
                print(f'Object {repr(obj)} fail -> "{e}"')

    is_not_none = IsNotNoneHandler()
    is_string = IsStringHandler()

    is_match_re_1 = IsMatchReHandler("\d")
    is_match_re_2 = IsMatchReHandler("1..")
    is_match_re_3 = IsMatchReHandler("\d{3}")
    is_match_re_1.set_next(is_match_re_2).set_next(is_match_re_3)

    # Check only None
    client_code(IsNotNoneHandler())
    print()

    # Check all
    is_not_none.set_next(is_string).set_next(is_match_re_1)
    client_code(is_not_none)
    print()

    # Check only is_match_re_3
    client_code(is_match_re_3)
