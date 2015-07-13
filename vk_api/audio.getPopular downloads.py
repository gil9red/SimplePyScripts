#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import vk_api
import sys
import requests
import urllib.parse


LOGIN = ''
PASSWORD = ''
DOWNLOAD_DIR = 'popular downloads'


# TODO: учитывать наличие разделения песен на альбомы
# TODO: возможность выбирать диапазоны индексов скачиваемых песен


def vk_auth(login, password):
    try:
        vk = vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as e:
        print(e)  # В случае ошибки выведем сообщение
        sys.exit()

    return vk


def get_audio_url_info(url):
    """Функция вернет принимает строку вида https://psv4.vk.me/c5124/u2165478/audios/327a9652ea58.mp3?extra=Bo-era...
    И возвращает кортеж, состоящий из адрес без параметра extra и формата файла:
    ('https://psv4.vk.me/c5124/u2165478/audios/327a9652ea58.mp3', '.mp3')

    """

    # Парсим
    result = urllib.parse.urlparse(url)

    # Собираем Url
    new_url = result.scheme + '://' + result.netloc + result.path

    # Вытаскиваем суффикс файла
    file_suffix = os.path.splitext(result.path)[-1]
    return new_url, file_suffix


def download_file(url, audio_name, dir_):
    # TODO: Замена символов, которых в названиях файлов запрещено
    # audio_file_name = audio_file_name.replace('"', '')

    # Путь в который будет скачен файл
    download_path = os.path.join(dir_, audio_name)

    # Попытаемся скачать аудиозапись
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Создаем файл и в него записываем файл с сервера
        with open(download_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        # TODO: кидать исключение при неудачи
        pass


if __name__ == '__main__':
    print('Авторизация...')

    try:
        # Авторизируемся
        vk = vk_auth(LOGIN, PASSWORD)

        # Получение аудиозаписей текущего пользователя (чей логин был введен)
        # Варианты значения genre_id: https://vk.com/dev/audio_genres
        # genre_id = 7 -- это Metal
        #            1 -- Rock
        #            21 -- Alternative
        data = {
            'genre_id': 7,
            'count': 1
        }
        list_audio = vk.method('audio.getPopular', data)

        # Если не существует пути, создадим его
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        for i, audio in enumerate(list_audio, 1):
            print(audio)
            url = audio['url']
            url, suffix = get_audio_url_info(url)
            name = '{artist} - {title}{0}'.format(suffix, **audio)
            print('{artist} - {title}{0} -> {1}'.format(suffix, url, **audio))
            print()

            print('{}. "{}"'.format(i, name), end='')
            download_file(url, name, DOWNLOAD_DIR)
            print(' download finished...')
        #     else:
        # #         print('Не получилось скачать "{}"...'.format(audio_name))

        # TODO: имя файла "<artist> - <title>".mp3
        # TODO: формат аудифайла определять по суффиксу url, скорее всего, всегда будет mp3


        #
        # # Вывод списка всех аудиозаписей
        # print('Всего песен: {}'.format(audio['count']))
        #
        # for i, a in enumerate(audio['items'][:1], 1):
        #     artist = a['artist']
        #     title = a['title']
        #     url = a['url']
        #     # duration = a['duration']
        #     # album_id = a.get('album_id')
        #
        #     audio_name = '{} - {}'.format(artist, title)
        #
        #     # Название файла аудиозаписи
        #     audio_file_name = audio_name + '.mp3'
        #
        #     # Замена символов, которых в названиях файлов запрещено
        #     # TODO: бОльший контроль, индивидуальный для ОС
        #     audio_file_name = audio_file_name.replace('"', '')
        #
        #     # Путь в который будет скачен файл
        #     download_path = os.path.join(DOWNLOAD_DIR, audio_file_name)
        #
        #     # Попытаемся скачать аудиозапись
        #     r = requests.get(url, stream=True)
        #     if r.status_code == 200:
        #         print('{}. "{}"'.format(i, audio_name), end='')
        #
        #         # Создаем файл и в него записываем файл с сервера
        #         with open(download_path, 'wb') as f:
        #             for chunk in r.iter_content(1024):
        #                 f.write(chunk)
        #
        #         print(' download finished...')
        #
        #     else:
        #         print('Не получилось скачать "{}"...'.format(audio_name))

    except KeyboardInterrupt:
        print('\n\nСкачивание прервано.')
        sys.exit()
