#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


"""Скрипт подсчитывает количество слов в тексте."""


import re
from collections import Counter


text = """Конечно, там еще много работы. Нужно корректно переводить слова с несколькими значениями, улучшать перевод
разных форм глаголов, сделать настраиваемый уровень перевода для разных уровней владения английским, готовить
упражнения для запоминания новых слов. Этим я буду заниматься на досуге в ближайшие месяцы. """

# Ищем слова в кирилице
for i, match in enumerate(re.finditer(r"[а-яА-Я]+", text), 1):
    print(i, match)

print()

# Разделяем текст по любым символам, кроме буквенного или цифрового символа или знака подчёркивания
found = re.split(r"\W+", text)
found = [c for c in found if c]
print(len(found), found)

print()

# Ищем буквенные или цифровые символы или знаки подчёркивания, имеющие границу
words = re.findall(r"\b\w+\b", text)
print("Words: %s\nCount: %s" % (words, len(words)))

word_count = Counter(words)
for word, c in word_count.items():
    print("'%s': %s" % (word, c))
