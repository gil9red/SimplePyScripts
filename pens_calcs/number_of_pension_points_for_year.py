#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import common


# http://www.pfrf.ru/thm/common/mod/pensCalc/js/cash.js
def number_of_pension_points_for_year(zp: float) -> float:
    """
    Функция для подсчета количества пенсионных баллов за год.

    :param zp: заработная плата до вычета НДФЛ
    :return:
    """

    if zp > common.ZPM:
        zp = common.ZPM

    # Зарплата меньше мрот
    if zp < common.MROT:
        raise Exception(
            "Ошибка! Введите зарплату выше, чем минимальный размер оплаты труда в "
            "Российской Федерации в 2017 году - 7 500 рублей"
        )

    kpk_trud = zp / common.ZPM * 10
    if kpk_trud > 8.26:
        kpk_trud = 8.26

    return round(kpk_trud * 100) / 100


if __name__ == "__main__":
    # Сколько пенсионных баллов может быть начислено Вам за 2017 год?
    #
    # Введите размер Вашей ежемесячной заработной платы до вычета НДФЛ:
    #
    # Результаты расчета
    # Количество пенсионных баллов за год:
    #
    print(number_of_pension_points_for_year(7500))  # 1.03
    assert number_of_pension_points_for_year(7500) == 1.03

    print(number_of_pension_points_for_year(35000))  # 4.79
    assert number_of_pension_points_for_year(35000) == 4.79

    print(number_of_pension_points_for_year(60000))  # 8.22
    assert number_of_pension_points_for_year(60000) == 8.22

    print(number_of_pension_points_for_year(80000))  # 8.26
    assert number_of_pension_points_for_year(80000) == 8.26
