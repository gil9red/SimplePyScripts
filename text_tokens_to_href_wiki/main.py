#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import string

from pathlib import Path


DIR = Path(__file__).resolve().parent
DIR_RESULT = DIR / 'result'
DIR_RESULT.mkdir(parents=True, exist_ok=True)


BASE_URL = 'https://ru.wikipedia.org/wiki/'
CHAR_TO_DESCRIPTION = {
    ' ': 'Пробел',
    '\n': 'Перевод_строки',
    '\t': 'Табуляция',
}


def _on_match(m: re.Match) -> str:
    token = m.group()
    token_in_url = CHAR_TO_DESCRIPTION.get(token, token)
    return f'<a href="{BASE_URL}{token_in_url}">{token}</a>'


def process(text: str) -> str:
    return re.sub(r'\w+|\s+|[%s]' % string.punctuation, _on_match, text)


if __name__ == '__main__':
    text = "Съешь ещё этих мягких французских булок, да выпей чаю"
    text = process(text)

    f = DIR_RESULT / 'wiki.html'
    f.write_text(text, encoding='utf-8')
