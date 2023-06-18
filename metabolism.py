#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Формулы для вычисления обмена веществ
"""


import enum


@enum.unique
class FactorEnum(enum.Enum):
    # Сидячий образ жизни. Минимум нагрузки
    V_12 = 1.2

    # Небольшая физическая нагрузка/занятия спортом 1-3 в неделю
    V_1375 = 1.375

    # Достаточно большая физическая нагрузка/занятия спортом 3-5 в неделю
    V_155 = 1.55

    # Большая физическая нагрузка/занятия спортом 6-7 раз в неделю
    V_1725 = 1.725

    # Очень большая ежедневная физическая нагрузка/занятия спортом 2 раза в день
    V_19 = 1.9


def get_1918_for_male(
    weight_kg: int, height_cm, age: int, factor: FactorEnum = FactorEnum.V_12
) -> int:
    """
    Формула-Уравнение Харриса-Бенедикта для мужчин.
    """
    value = (13.7416 * weight_kg) + (5.0033 * height_cm) - (6.7500 * age) + 66.4730
    return int(value * factor.value)


def get_1918_for_female(
    weight_kg: int, height_cm, age: int, factor: FactorEnum = FactorEnum.V_12
) -> int:
    """
    Формула-Уравнение Харриса-Бенедикта для женщин.
    """
    value = (9.5634 * weight_kg) + (1.8496 * height_cm) - (4.6756 * age) + 665.0955
    return int(value * factor.value)


def get_1984_for_male(
    weight_kg: int, height_cm, age: int, factor: FactorEnum = FactorEnum.V_12
) -> int:
    """
    Пересмотренная Формула-Уравнение Харриса-Бенедикта для мужчин.
    """
    value = (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age) + 88.362
    return int(value * factor.value)


def get_1984_for_female(
    weight_kg: int, height_cm, age: int, factor: FactorEnum = FactorEnum.V_12
) -> int:
    """
    Пересмотренная Формула-Уравнение Харриса-Бенедикта для женщин.
    """
    value = (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age) + 447.593
    return int(value * factor.value)


def get_2005_for_male(
    weight_kg: int, height_cm, age: int, factor: FactorEnum = FactorEnum.V_12
) -> int:
    """
    Формула-Уравнение Миффлина-Санкт-Джеора для мужчин.
    """
    value = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    return int(value * factor.value)


def get_2005_for_female(
    weight_kg: int, height_cm, age: int, factor: FactorEnum = FactorEnum.V_12
) -> int:
    """
    Формула-Уравнение Миффлина-Санкт-Джеора для женщин.
    """
    value = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    return int(value * factor.value)


if __name__ == "__main__":
    weight_kg = 100
    height_cm = 190
    age = 30

    print("male (1918):", get_1918_for_male(weight_kg, height_cm, age))
    print("female (1918):", get_1918_for_female(weight_kg, height_cm, age))
    # male (1918): 2626
    # female (1918): 2199

    print()

    print("male 1984:", get_1984_for_male(weight_kg, height_cm, age))
    print("female 1984:", get_1984_for_female(weight_kg, height_cm, age))
    # male 1984: 2603
    # female 1984: 2197

    print()

    print("male 2005:", get_2005_for_male(weight_kg, height_cm, age))
    print("female 2005:", get_2005_for_female(weight_kg, height_cm, age))
    # male 2005: 2451
    # female 2005: 2251
