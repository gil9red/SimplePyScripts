#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://shultais.education/blog/python-f-strings


from datetime import datetime as dt
from math import pi


name = "Дмитрий"
age = 25
print(f"Меня зовут {name} Мне {age} лет.")
print()

print("# f-строки также поддерживают расширенное форматирование чисел:")
print(f"Значение числа pi: {pi:.2f}")
print()

print("# С помощью f-строк можно форматировать дату без вызова метода strftime():")

print(f"Текущее время {dt.now():%d.%m.%Y %H:%M}")
now = dt.now()
print(f"Текущее время {now:%d.%m.%Y %H:%M}")
print()

print("# Они поддерживают базовые арифметические операции. Да, прямо в строках:")
x = 10
y = 5
print(f"{x} x {y} / 2 = {x * y / 2}")
print()

print("# Позволяют обращаться к значениям списков по индексу:")
planets = ["Меркурий", "Венера", "Земля", "Марс"]
print(f"Мы живим не планете {planets[2]}")
print()

print("# А также к элементам словаря по ключу:")
planet = {"name": "Земля", "radius": 6378000}
print(f"Планета {planet['name']}. Радиус {planet['radius']/1000} км.")
print()

print(
    "# Причем вы можете использовать как строковые, так и числовые ключи. "
    "Точно также как в обычном Python коде:"
)
digits = {0: "ноль", "one": "один"}
print(f"0 - {digits[0]}, 1 - {digits['one']}")
print()

print("# Вы можете вызывать в f-строках методы объектов:")
name = "Дмитрий"
print(f"Имя: {name.upper()}")
print()

print("# А также вызывать функции:")
print(f"13 / 3 = {round(13/3)}")
