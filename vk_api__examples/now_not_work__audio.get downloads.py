# !/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import os
import vk_api
import sys
import requests
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.id3 import TIT2, TPE1


# https://github.com/python273/vk_api
# https://vk.com/dev/methods
# http://vk.com/dev/audio.getAlbums
# http://vk.com/dev/audio.get


# Download audio user
# Скачивание аудиозаписей пользователя


# TODO: учитывать наличие разделения песен на альбомы
# TODO: возможность выбирать диапазоны индексов скачиваемых песен


def make_pretty_id3(audio_file_name, performer, title_):
    """Функция удаляет из тега фреймы (COMM, PRIV, ...), добавляет (а если есть переписывает)
    фреймы TPE1 (имя группы) и TIT2 (название песни)

    """

    def get_id3_frame(id3, frame):
        try:
            return id3[frame]
        except KeyError:
            return None

    audio = ID3()

    try:
        audio.load(audio_file_name)

        album = get_id3_frame(audio, 'TALB')
        genre = get_id3_frame(audio, 'TCON')
        record_time = get_id3_frame(audio, 'TDRC')
        picture = get_id3_frame(audio, 'APIC')

        audio.delete()

        audio.add(TPE1(3, performer))
        audio.add(TIT2(3, title_))

        if album is not None:
            audio.add(album)

        if genre is not None:
            audio.add(genre)

        if record_time is not None:
            audio.add(record_time)

        if picture is not None:
            audio.add(picture)

    except ID3NoHeaderError:
        audio.add(TPE1(3, performer))
        audio.add(TIT2(3, title_))

    audio.save()


class DownloadFileError(Exception):
    pass


def download_file(url, audio_file_name):
    # Попытаемся скачать аудиозапись
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Создаем файл и в него записываем файл с сервера
        with open(audio_file_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise DownloadFileError('Ошибка при скачивании "{}": {} - {}'.format(url, r.status_code, r.reason))


LOGIN = ''
PASSWORD = ''
DOWNLOAD_DIR = 'downloads'


if __name__ == '__main__':
    print('Авторизация...')
    print()

    try:
        vk = vk_api.VkApi(LOGIN, PASSWORD)
        vk.auth()  # Авторизируемся

        # Получение аудиозаписей текущего пользователя (чей логин был введен)
        # Для получения аудиозаписей определенного пользователя нужно передавать
        # его id, например: audio = vk.method('audio.get', {'owner_id': '170968205'})
        audio = vk.method('audio.get')

    except Exception as e:
        print(e)
        sys.exit()

    # # Получаем альбомы пользователя
    # albums = vk.method('audio.getAlbums')['items']
    # print(albums)
    #
    # albums = {
    #     a['id']: a['title']
    #     for a in albums
    # }
    # print(albums)

    # Если не существует пути, создадим его
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Вывод списка всех аудиозаписей
    print('Всего песен: {}'.format(audio['count']))

    list_audio = audio['items']

    for i, audio in enumerate(list_audio, 1):
        try:
            artist = audio['artist'].strip().title()
            title = audio['title'].strip().capitalize()
            url = audio['url']
            # duration = a['duration']
            # album_id = a.get('album_id')

            audio_name = '{} - {}'.format(artist, title)

            # Название файла аудиозаписи
            audio_file_name = audio_name + '.mp3'

            # Замена символов, которых в названиях файлов запрещено
            # TODO: бОльший контроль, индивидуальный для ОС
            audio_file_name = audio_file_name.replace('"', '')

            # Путь в который будет скачен файл
            download_path = os.path.join(DOWNLOAD_DIR, audio_file_name)

            if os.path.exists(download_path):
                print('File is exist: {}'.format(download_path))
                continue

            print('{}. "{}"'.format(i, audio_name), end='')
            download_file(url, download_path)
            make_pretty_id3(download_path, artist, title)
            print(' download finished...')

        except KeyboardInterrupt:
            print('\n\nСкачивание прервано.')
            sys.exit()

        except Exception as e:
            print('audio id={} owner_id={}, error: {}'.format(audio['id'], audio['owner_id'], e))
