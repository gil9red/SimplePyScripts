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

    def __init__(self, start_time: str, duration: int):
        self.start = DT.datetime.strptime(start_time, '%H:%M:%S')
        self.end = self.start + DT.timedelta(seconds=duration)

    def is_contains(self, datetime: DT.datetime) -> bool:
        return self.start <= datetime <= self.end

    def __repr__(self) -> str:
        return f'<{self.start:%H:%M:%S} - {self.end:%H:%M:%S}>'


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
        Interval('12:00:00', 20 * 60),
        Interval('12:10:00', 10 * 60),
        Interval('12:15:00', 30 * 60),
        Interval('13:00:00', 30 * 60),
    ]
    print(find_max_intersection(items))
    # 3
