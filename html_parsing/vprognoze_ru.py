#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback

# pip install selenium
from selenium import webdriver


URL = "https://vprognoze.ru/"

driver = webdriver.Firefox()
try:
    driver.implicitly_wait(5)
    driver.get(URL)
    print(f"Title: {driver.title!r}")

    for a in driver.find_elements_by_css_selector(".title_news > a"):
        print(a.text)
    # Фьолнир - Валюр от Football2020 | 27-07-2020
    # Стьярнан - Викингур Рейкьявик от Football2020 | 27-07-2020
    # Хаммарбю - Эребру | Беневенто - Кьево | Кротоне - Фрозиноне от Sailor1263
    # Арсенал - Челси | 01-08-2020 от Footbets11
    # Фьолнир - Валюр от Limonchello | 27-07-2020
    # Саннес - Улл/Киса | 27-07-2020 от Football2020
    # Фаллон Шэррок (Анг) - Хосе Антонио Хустисия Пералес (Исп) | 27-07-2020 от riadik2000
    # Стьордалс-Блинк - Стреммен | 27-07-2020 от Football2020
    # ФК Торонто - Нью-Йорк Сити | 27-07-2020 от Limonchello
    # Микульските - Маринкович от RunnerUp | 27-07-2020
    # Тяньцзинь Жунган - Гуанчжоу Лонг Лайонс от genii1978 | 27-07-2020
    # Хосе Антонио Хустисия Пералес (Исп) - Скотт Марш (Анг) | 27-07-2020 от riadik2000
    # Nigma - FlytoMoon от Artorias | 27-07-2020

except:
    print(traceback.format_exc())

finally:
    driver.quit()
