#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: function from languagetool/check.py
def check_ru(text: str) -> list():
    """
    Функция делает запрос на https://languagetool.org/ чтобы проверить на правильность указанный текст.
    Если возвращается пустой массив -- проблем не было найдено, иначе -- есть.
    В возращаемом списке можно узнать что именно не понравилось languagetool и варианты исправления.

    """

    url = 'https://languagetool.org/api/v2/check'
    post_data = {
        'disabledRules': 'WHITESPACE_RULE',
        'allowIncompleteResults': 'true',
        'text': text,
        'language': 'ru',
    }

    import requests
    rs = requests.post(url, data=post_data)
    if not rs.ok:
        raise Exception(f'Проблема с {url}, status_code = {rs.status_code}')

    return rs.json()['matches']


# NOTE: file tags.json from stackoverflow/download_tags.py
import json
tags = json.load(open('tags.json', 'r', encoding='utf-8'))

import time

for tag, value in sorted(tags.items(), key=lambda x: len(x[1]['description'])):
    print(tag)

    text = value['description']

    while True:
        try:
            matches = check_ru(text)
            if matches:
                print(tag, value['url_info'], len(text))

                print('Найденные проблемы:')
                for match in matches:
                    error = match['message']
                    context = match['context']
                    offset = context['offset']
                    length = context['length']

                    error_text = context['text'][offset: offset + length]
                    replacements = [i['value'] for i in match['replacements']]
                    print(f'"{error_text}" [{offset}:{length}]: "{error}" -> {replacements}')

                print('\n')
                print('-' * 50)
                print('\n')

            break

        except Exception as e:
            import traceback
            print(f"ERROR: '{e}'\n\n{traceback.format_exc()}")

            time.sleep(10)

    time.sleep(5)
