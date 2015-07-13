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


# TODO: проверять песни на уникальность -- возможно они будут повторяться


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


class DownloadFileError(Exception):
    pass


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
        raise DownloadFileError('Ошибка при скачивании "{}": {} - {}'.format(url, r.status_code, r.reason))


if __name__ == '__main__':
    print('Авторизация...')

    try:
        # Авторизируемся
        vk = vk_api.VkApi(LOGIN, PASSWORD)

        # Варианты значений data:
        #     only_eng	1 – возвращать только зарубежные аудиозаписи. 0 – возвращать все аудиозаписи. (по умолчанию)
        #     genre_id	идентификатор жанра из списка жанров (https://vk.com/dev/audio_genres)
        #     offset	смещение, необходимое для выборки определенного подмножества аудиозаписей.
        #     count	количество возвращаемых аудиозаписей (максимальное значение 1000, по умолчанию 100).

        data = {
            'genre_id': 7,  # Metal
            'count': 5
        }
        list_audio = vk.method('audio.getPopular', data)

        # Если не существует пути, создадим его
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        for i, audio in enumerate(list_audio, 1):
            url = audio['url']
            url, suffix = get_audio_url_info(url)
            name = '{artist} - {title}{0}'.format(suffix, **audio)

            print('{}. "{}"'.format(i, name), end='')
            download_file(url, name, DOWNLOAD_DIR)
            print(' download finished...')

    except DownloadFileError as e:
        print(e)

    except vk_api.AuthorizationError as e:
        print(e)
        sys.exit()

    except KeyboardInterrupt:
        print('\n\nСкачивание прервано.')
        sys.exit()
