#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дана частичная выборка из датасета зафиксированных преступлений, совершенных в городе Чикаго с 2001 года
по настоящее время.

Одним из атрибутов преступления является его тип – Primary Type.

Вам необходимо узнать тип преступления, которое было зафиксировано максимальное число раз в 2015 году.

Файл с данными:
Crimes.csv

"""


if __name__ == "__main__":
    import csv
    from collections import Counter

    with open("Crimes.csv") as csvfile:
        reader = csv.DictReader(csvfile)

        # Фильтр по 2015 году
        select_by_2015_year = filter(lambda x: "2015" in x["Date"], reader)

        # Список словарей с преступлениями делаем списком с типом преступлений и подсчитываем их количество
        counter = Counter(x["Primary Type"] for x in select_by_2015_year)

        # Сортировка по количеству преступлений
        primary_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)

        # Вытаскиваем самое частое преступление
        print(*primary_counter[0])
