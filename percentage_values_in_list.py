#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
https://ru.stackoverflow.com/questions/510347

Есть некий список с возрастающими данными: [30, 42, 49, 50, 65, 104, 420, 404, 513, ...].
Задача: подсчитать в процентном соотношении размер (ширину) каждого значения (элемента) в списке. Список может
динамически пополняться новым значением при помощи .push().

Пример:
Есть список: [100, 100] - получаем размер значений: [50%, 50%]

Добавляем новое значение: .push(200) - [100, 100, 200]
Получаем: [25%, 25%, 50%]

Добавляем значение: .push(400) - [100, 100, 200, 400]
Получаем: [12.5%, 12.5%, 25%, 50%]
"""


def get_percentage_values(items):
    """Возвращает список с процентным значением элемента списка."""

    sum_items = sum(items)
    return [f"{i / sum_items * 100:.1f}%" for i in items]


if __name__ == "__main__":
    print(get_percentage_values([100, 100]))
    print(get_percentage_values([100, 100, 200]))
    print(get_percentage_values([100, 100, 200, 400]))
    print(get_percentage_values([30, 42, 49, 50, 65, 104, 420, 404, 513]))
