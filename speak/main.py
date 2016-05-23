#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def bing_speak(text, locale, gender='female'):
    """
    Функция выполняет запрос в bing сервис синтезирования речи и возвращает получившийся mp3-файл с речью
    в виде байтовой строки.

    """

    # Примеры запросов в сервис синтезирования речи:
    # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=male&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA
    # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=female&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA

    url = 'http://www.bing.com/translator/api/language/Speak'
    params = {
        'locale': locale,
        'gender': gender,
        'media': 'audio/mp3',
        'text': text,
    }

    import requests
    s = requests.Session()

    # Получим куки, иначе получим ошибку: {"message": "Service unavailable. Please try again later."}
    rs = s.get('http://www.bing.com/translator')
    if not rs.ok:
        raise Exception('Error [%s]: %s.', rs.status_code, rs.text)

    rs = s.get(url, params=params)
    if not rs.ok:
        raise Exception('Error [%s]: %s.', rs.status_code, rs.text)

    return rs.content


if __name__ == '__main__':
    # # Для логирования запросов requests:
    # import logging
    # import sys
    # logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    text = 'Сорок тысяч обезьян в жопу сунули банан'

    with open('speak_female.mp3', 'wb') as f:
        female_mp3_content = bing_speak(text, 'ru-RU')
        f.write(female_mp3_content)

    with open('speak_male.mp3', 'wb') as f:
        male_mp3_content = bing_speak(text, 'ru-RU', gender='male')
        f.write(male_mp3_content)
