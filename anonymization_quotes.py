#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import string


def anonymization_quotes(quote_text):
    """
    Функция заменяет ники в цитатах на псевдонимы 'xxx', 'yyy' и т.п.
    Шаблон определения "^(.+?):"

    Пример валидной цитаты: "BlackFox: Кто нибудь, хоть раз, физически ощущал как он седеет?..."

    """

    login_pattern = re.compile(r"^(.+?):")

    # Словарь, в котором ключом является логин, а значением псевдоним
    all_logins = dict()

    # Счетчик логинов
    count_logins = 0

    # Сгенерируем список с псевдонимами. Список будет вида: ['aaa', 'bbb', ..., 'zzz', 'AAA', ... 'ZZZ']
    login_aliases = [c * 3 for c in string.ascii_letters]

    # Разбиваем цитату по строчно
    for line in quote_text.split("\n"):
        # Ищем логин
        match = login_pattern.search(line)

        # Если нашли
        if match:
            # Вытаскиваем только логин -- нам не нужно двоеточние после логина
            login = match.group(1)

            # Если такого логина нет в словаре, добавляем в словарь логин и его псевдоним
            if login not in all_logins:
                all_logins[login] = login_aliases[count_logins]
                count_logins += 1

    quote = quote_text

    # Проходим по словарю и делаем замену логина на псевдоним в строке цитаты
    for login, alias in all_logins.items():
        quote = quote.replace(login, alias)

    return quote


if __name__ == "__main__":
    quote = """
Аня: Не хочу и комп занят
Кирилл: вредный старший брат окупировал комп?
Кирилл: у моей сестры таже проблема
"""

    print(quote)

    quote = anonymization_quotes(quote)
    print()
    print(quote)
