#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
В колл-центре ведётся журнал исходящих звонков.
Каждому звонку соответствует запись вида
<Дата и время начала интервью><Длительность интервью>
На языке Python напишите фрагмент программы, который определяет максимальное
число одновременных телефонных интервью за всю историю. Т.е. фактически максимальное число занятых
телефонных линий.
"""


import datetime as DT
from typing import List


# Класс (структура) для хранения интервала звонка
class Interval:
    start: DT.datetime
    end: DT.datetime

    def __init__(self, start: DT.datetime, duration: int):
        self.start = start
        self.end = self.start + DT.timedelta(seconds=duration)

    def is_contains(self, datetime: DT.datetime) -> bool:
        return self.start <= datetime <= self.end

    def __str__(self):
        return f'<{self.start} - {self.end}>'


def find_max_intersection(items: List[Interval]) -> int:
    max_value = 0

    for interval in items:
        # Подсчет количества пересечений
        count = sum(x.is_contains(interval.start) for x in items)

        # Нахождение максимума
        if count > max_value:
            max_value = count

    return max_value


if __name__ == '__main__':
    items = [
        Interval(DT.datetime(2021, 4, 21, 12, 0, 0),  20 * 60),
        Interval(DT.datetime(2021, 4, 21, 12, 10, 0), 10 * 60),
        Interval(DT.datetime(2021, 4, 21, 12, 15, 0), 30 * 60),
        Interval(DT.datetime(2021, 4, 21, 13, 0, 0),  30 * 60),
    ]
    print(find_max_intersection(items))
    # 3
