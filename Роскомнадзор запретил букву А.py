#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


alp = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
result = "Роскомнадзор запретил букву "

# Перебор всех символов алфавита
for c in alp:
    # Проверяем, что в строке result текущая буква найдена
    if c in result or c.upper() in result:
        # Выводим надпись
        print(result + c.upper())

        # Удаляем букву из надписи
        result = result.replace(c, "")
        result = result.replace(c.upper(), "")
