#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from itertools import chain
from utils import get_report_persons_info, get_person_info


report_dict = get_report_persons_info()

# Вывести всех сотрудников, отсортировав их по количестве переработанных часов
person_list = set(chain(*report_dict.values()))

# Проверка того, что сортировка работает (в принципе, думаю можно удалить)
assert sorted(person_list, key=lambda x: x.deviation_of_time) == sorted(
    person_list, key=lambda x: x.deviation_of_time.total
)

sorted_person_list = sorted(
    person_list, key=lambda x: x.deviation_of_time, reverse=True
)

for i, person in enumerate(sorted_person_list, 1):
    print(f"{i:>3}. {person.full_name} {person.deviation_of_time}")

print()
person = get_person_info(
    second_name="Петраш", first_name="Илья", report_dict=report_dict
)
if person:
    print(
        f"#{sorted_person_list.index(person) + 1}. {person.full_name} {person.deviation_of_time}"
    )
