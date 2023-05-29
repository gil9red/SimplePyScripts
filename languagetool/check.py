#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт использует вебсервис languagetool.org, основанный на LanguageTool,
для проверки проверки грамматики, пунктуации, орфографии и стиля.

Сайт: https://www.languagetool.org/ru/
Гитхаб: https://github.com/languagetool-org/

"""


import requests


def check_ru(text: str) -> list():
    """
    Функция делает запрос на https://languagetool.org/ чтобы проверить на правильность указанный текст.
    Если возвращается пустой массив -- проблем не было найдено, иначе -- есть.
    В возращаемом списке можно узнать что именно не понравилось languagetool и варианты исправления.

    """

    url = "https://languagetool.org/api/v2/check"
    post_data = {
        "disabledRules": "WHITESPACE_RULE",
        "allowIncompleteResults": "true",
        "text": text,
        "language": "ru",
    }

    rs = requests.post(url, data=post_data)
    if not rs.ok:
        raise Exception("Проблема с {}, status_code = {}".format(url, rs.status_code))

    return rs.json()["matches"]


def is_ok_ru(text: str) -> bool:
    """
    Функция возвращает True, если проблем в тексте не найдено, иначе -- False.

    """

    return not check_ru(text)


if __name__ == "__main__":
    text = """\
Интересует другое почему она возникла?
Дубаль два, надеюсь все пройдет отлично.
Не навижу делать ключи для геологаций карт, меня это раздражает сильно:rage:.
"""

    matches = check_ru(text)
    if not matches:
        print("Ошибок нет")
    else:
        print("Найденные проблемы:")

        for match in matches:
            error = match["message"]
            context = match["context"]
            offset = context["offset"]
            length = context["length"]

            error_text = context["text"][offset : offset + length]
            print(
                '"{}" [{}:{}]: "{}" -> {}'.format(
                    error_text,
                    offset,
                    length,
                    error,
                    [i["value"] for i in match["replacements"]],
                )
            )

    print()
    print("-" * 20)
    print(is_ok_ru(text))
    print(is_ok_ru("Все хорошо!"))

    # NOTE: пример массива из check_ru при тексте с ошибками:
    # rs = {'warnings': {'incompleteResults': False}, 'language': {'code': 'ru-RU', 'name': 'Russian'}, 'software': {'apiVersion': '1', 'buildDate': '2017-03-01 21:01', 'name': 'LanguageTool', 'version': '3.7-SNAPSHOT', 'status': ''}, 'matches': [{'message': 'Не найдены обязательные зависимые слова: интересовать кого?', 'offset': 0, 'length': 17, 'context': {'length': 17, 'offset': 0, 'text': 'Интересует другое почему она возникла? Дубаль два, надеюс...'}, 'rule': {'subId': '2', 'description': 'Пропуск обязательных зависимых слов', 'issueType': 'uncategorized', 'category': {'name': 'Стиль', 'id': 'STYLE'}, 'id': 'strong_m'}, 'shortMessage': 'интересовать кого?', 'replacements': []}, {'message': 'Найдена орфографическая ошибка', 'offset': 39, 'length': 6, 'context': {'length': 6, 'offset': 39, 'text': 'Интересует другое почему она возникла? Дубаль два, надеюсь все пройдет отлично. Не на...'}, 'rule': {'description': 'Проверка орфографии с исправлениями', 'issueType': 'misspelling', 'category': {'name': 'Проверка орфографии', 'id': 'TYPOS'}, 'id': 'MORFOLOGIK_RULE_RU_RU'}, 'shortMessage': 'Орфографическая ошибка', 'replacements': [{'value': 'Дубль'}, {'value': 'Дубась'}]}, {'message': 'Найдена орфографическая ошибка', 'offset': 83, 'length': 6, 'context': {'length': 6, 'offset': 43, 'text': '...ль два, надеюсь все пройдет отлично. Не навижу делать ключи для геологаций карт, меня ...'}, 'rule': {'description': 'Проверка орфографии с исправлениями', 'issueType': 'misspelling', 'category': {'name': 'Проверка орфографии', 'id': 'TYPOS'}, 'id': 'MORFOLOGIK_RULE_RU_RU'}, 'shortMessage': 'Орфографическая ошибка', 'replacements': [{'value': 'нанижу'}, {'value': 'насижу'}, {'value': 'навиду'}, {'value': 'навису'}, {'value': 'навожу'}, {'value': 'навяжу'}, {'value': 'новику'}, {'value': 'новину'}, {'value': 'завижу'}, {'value': 'на вижу'}]}, {'message': 'Найдена орфографическая ошибка', 'offset': 107, 'length': 10, 'context': {'length': 10, 'offset': 43, 'text': '...дет отлично. Не навижу делать ключи для геологаций карт, меня это раздражает сильно:rage:....'}, 'rule': {'description': 'Проверка орфографии с исправлениями', 'issueType': 'misspelling', 'category': {'name': 'Проверка орфографии', 'id': 'TYPOS'}, 'id': 'MORFOLOGIK_RULE_RU_RU'}, 'shortMessage': 'Орфографическая ошибка', 'replacements': [{'value': 'геологами'}, {'value': 'геологии'}, {'value': 'геологий'}, {'value': 'омологации'}]}]}
    # print(rs)
    # print(rs['matches'])
