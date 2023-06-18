#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from itertools import groupby
from typing import Iterable, Callable


def split_by_func(items: Iterable, func: Callable) -> list[list]:
    return [list(x[1]) for x in groupby(items, func) if not x[0]]


if __name__ == "__main__":
    items = "123-456-789"
    parts = split_by_func(items, lambda x: x == "-")
    print(parts)
    # [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

    items = ["123", "-", "456", "-", "789"]
    parts = split_by_func(items, lambda x: x == "-")
    print(parts)
    # [['123'], ['456'], ['789']]

    tokens = [
        "Сообщество",
        "здесь",
        ",",
        "чтобы",
        "помочь",
        "вам",
        "с",
        "конкретными",
        "проблемами",
        "по",
        "программированию",
        ",",
        "алгоритмам",
        ",",
        "языкам",
        "программирования",
        ".",
    ]
    parts = split_by_func(tokens, lambda x: x in ",.")
    print(parts)
    # [['Сообщество', 'здесь'], ['чтобы', 'помочь', 'вам', 'с', 'конкретными',
    # 'проблемами', 'по', 'программированию'], ['алгоритмам'], ['языкам', 'программирования']]
