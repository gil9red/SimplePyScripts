#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install fuzzywuzzy[speedup]
from fuzzywuzzy import process


OPTS = {
    "Find"   : ('найти', 'найди', 'искать', 'поиск'),
    "Add"    : ('добавить', 'добавь', 'добавляй', 'добавишь'),
    "Delete" : ('удалить', 'удали', 'убрать', 'убери'),
    "Correct": ('корректировать', 'скорректируй', 'скоректируй')
}


def select_command(text: str, min_score=80) -> str:
    for command, aliases in OPTS.items():
        score = process.extractOne(text, aliases)[1]
        if score >= min_score:
            return command


for text in ['найти', 'НАЙТИ', 'найДи', 'Наайди', 'удалЕ', 'убИри', 'коректирровать']:
    print(select_command(text))
# Find
# Find
# Find
# Find
# Delete
# Delete
# Correct
