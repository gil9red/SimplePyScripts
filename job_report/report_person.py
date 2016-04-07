#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from functools import total_ordering


class ReportPerson:
    """Класс для описания сотрудника в отчете."""

    def __init__(self, tags):
        # ФИО
        self.second_name, self.first_name, self.middle_name = tags[0].split()

        # Невыходов на работу
        self.absence_from_work = int(tags[1])

        # По календарю (смен / ч:мин)
        # Для точного значения посещенных дней, может быть указано как "3 = 4- (1 О)", поэтому
        # отсекаем правую, от знака равно, сторону, удаляем пробелы и переводим в число
        self.need_to_work_days = self.get_work_day(tags[2])
        self.need_to_work_on_time = self.get_work_time(tags[3])

        # Фактически (смен / ч:мин)
        self.worked_days = self.get_work_day(tags[4])
        self.worked_time = self.get_work_time(tags[5])

        # Отклонение (смен / ч:мин)
        self.deviation_of_day = self.get_work_day(tags[6])
        self.deviation_of_time = self.get_work_time(tags[7])

    @property
    def full_name(self):
        return self.second_name + ' ' + self.first_name + ' ' + self.middle_name

    @staticmethod
    def get_work_day(day_str):
        return int(day_str) if '=' not in day_str else int(day_str.split('=')[0].strip())

    @total_ordering
    class Time:
        """Простой класс для хранения даты работы."""

        def __init__(self, time_str):
            self._hours, self._minutes = map(int, time_str.split(':'))

        @property
        def total(self):
            """Всего минут"""

            return self._hours * 60 + self._minutes

        def __repr__(self):
            return "{:0>2}:{:0>2}".format(self._hours, self._minutes)

        def __eq__(self, other):
            return self.total == other.total

        def __lt__(self, other):
            return self.total < other.total

    @staticmethod
    def get_work_time(time_str):
        return ReportPerson.Time(time_str)

    def __repr__(self):
        return "{}. Невыходов на работу: {}. По календарю ({} смен / {} ч:мин). " \
               "Фактически ({} смен / {} ч:мин) Отклонение ({} смен / {} ч:мин)".format(self.full_name,
                                                                                        self.absence_from_work,
                                                                                        self.need_to_work_days,
                                                                                        self.need_to_work_on_time,
                                                                                        self.worked_days,
                                                                                        self.worked_time,
                                                                                        self.deviation_of_day,
                                                                                        self.deviation_of_time,
                                                                                        )
