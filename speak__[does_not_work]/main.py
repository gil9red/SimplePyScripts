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
    # Для логирования запросов requests:
    import logging
    import sys
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format='[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s',
    )

    text = 'Сорок тысяч обезьян в жопу сунули банан'

    logging.debug('Text: "%s".', text)

    logging.debug('Female')
    female_file_name = 'speak_female.mp3'
    with open(female_file_name, 'wb') as f:
        female_mp3_content = bing_speak(text, 'ru-RU')
        f.write(female_mp3_content)

    logging.debug('Female play')
    from play_mp3 import play
    play(female_file_name)

    logging.debug('Male')
    male_file_name = 'speak_male.mp3'
    with open(male_file_name, 'wb') as f:
        male_mp3_content = bing_speak(text, 'ru-RU', gender='male')
        f.write(male_mp3_content)

    logging.debug('Male play')
    play(male_file_name)
