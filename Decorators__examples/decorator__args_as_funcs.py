#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class TextBuilder:
    def __init__(self) -> None:
        self.result = []

    # Функция, принимающая аргументы и возвращающая декоратор
    def _call_before(*funcs):
        # Сам декоратор
        def decorator(func):
            # Функция-обертка, заменит собой декорируемую
            def wrapper(self, *args, **kwargs):
                for f in funcs:
                    f(self)

                return func(self, *args, **kwargs)

            # Декоратор возвращает обертку
            return wrapper

        # Возвращаем сам декоратор
        return decorator

    # Функция, принимающая аргументы и возвращающая декоратор
    def _call_after(*funcs):
        # Сам декоратор
        def decorator(func):
            # Функция-обертка, заменит собой декорируемую
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)

                for f in funcs:
                    f(self)

                return result

            # Декоратор возвращает обертку
            return wrapper

        # Возвращаем сам декоратор
        return decorator

    @_call_before(lambda self: self.result.append("+" + "-" * 10 + "+"))
    @_call_after(
        lambda self: self.result.append("+" + "-" * 10 + "+"),
        lambda self: self.result.append("\n"),
    )
    def append(self, text: str) -> "TextBuilder":
        self.result.append(text)
        return self

    def build(self):
        return "\n".join(self.result)


builder = TextBuilder()
builder.append("Foo").append("Bar").append("Hello World!")
print(builder.build())
# +----------+
# Foo
# +----------+
#
#
# +----------+
# Bar
# +----------+
#
#
# +----------+
# Hello World!
# +----------+
