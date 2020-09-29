#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://ru.stackoverflow.com/q/1184070/201445


import datetime as DT
from typing import Optional


SCHEDULE = {
    0: ['История', 'Биология', 'Химия', 'География', 'ИЗО', 'Технология', 'Алгебра'],
    1: ['Обществознание', 'Русский язык', 'Информатика(Малова)', 'Информатика(Чкалова)',
        'Музыка', 'Англ.яз (Якушева)', 'Англ.яз (Васильева)', 'Физ-ра'],
    2: ['Физика', 'Физ-ра', 'Химия', 'Литература', 'Русский язык', 'Алгебра',
        'Англ.яз (Якушева)', 'Англ.яз (Васильева)'],
    3: ['Русский язык', 'ОБЖ', 'Биология', 'Русский язык', 'Геометрия', 'Алгебра'],
    4: ['Литература', 'Физика', 'История', 'Алгебра', 'Англ.яз (Якушева)',
        'Англ.яз (Васильева)', 'Геометрия', 'География']
}


def get_nearest_lesson_date(lesson: str, d: DT.date = None) -> Optional[DT.date]:
    if not d:
        d = DT.date.today()

    lesson = lesson.lower()

    # Перебор дней недели
    for i in range(7):
        next_day = d + DT.timedelta(days=i+1)
        week_day = next_day.weekday()

        # Пропуск отсутствующих дней недели, например выходных
        if week_day not in SCHEDULE:
            continue

        # Регистронезависимый поиск предмета в списке
        if lesson in map(str.lower, SCHEDULE[week_day]):
            return next_day

    # Не нашли урок
    return


if __name__ == '__main__':
    print(get_nearest_lesson_date('Алгебра'))
    # 2020-09-30

    print(get_nearest_lesson_date('АЛГЕБРА'))
    # 2020-09-30

    d = get_nearest_lesson_date('изо', DT.date(2020, 9, 28))
    print(d)
    # 2020-10-05
    assert str(d) == '2020-10-05'

    d = get_nearest_lesson_date('Алгебра', DT.date(2020, 9, 29))
    print(d)
    # 2020-09-30
    assert str(d) == '2020-09-30'

    d = get_nearest_lesson_date('История', DT.date(2020, 10, 2))
    print(d)
    # 2020-10-05
    assert str(d) == '2020-10-05'

    d = get_nearest_lesson_date('ИЗО', DT.date(2020, 9, 26))
    print(d)
    # 2020-09-28
    assert str(d) == '2020-09-28'

    d = get_nearest_lesson_date('ИЗО', DT.date(2020, 9, 27))
    print(d)
    # 2020-09-28
    assert str(d) == '2020-09-28'

    d = get_nearest_lesson_date('ИЗО', DT.date(2020, 9, 28))
    print(d)
    # 2020-10-05
    assert str(d) == '2020-10-05'
