# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import vk_api
import sys
import requests
import urllib.parse
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.id3 import TIT2, TPE1


# TODO: реализовать механизм скачивания строго указанного количества песен
# в данной реализации из-за черного списка часть песен может не скачаться -- в запросе
# указывали 100 песен, а в итоге скачалось 90, поэтому нужно будет дополнительно отправлять
# запросы, пока не наберем указанное количество песен
# TODO: проверять песни на уникальность -- возможно они будут повторяться


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


def file_name_clear(name):
    """Функция удаляет и заменяет символы, которые в имени
    файлов windows не могут быть

    """

    # TODO: Замена символов, которых в названиях файлов запрещено
    # Windows: \/:*?"<>|

    name = name.replace('\\', '-')
    name = name.replace('/', '-')
    name = name.replace(':', '.')
    name = name.replace('*', '.')
    name = name.replace('?', '')
    name = name.replace('"', "'")
    name = name.replace('<', '')
    name = name.replace('>', '')
    name = name.replace('|', '')
    return name

# Список исполнителей, песни которых не хотим качать
_BLACK_LIST_ARTIST = []


def add_artist_to_black_list(artist):
    """Функция добавляет исполнителя в черный список."""
    _BLACK_LIST_ARTIST.append(artist.lower())


def artist_in_black_list(artist):
    """Функция вернет True, если исполнитель в черном списке."""
    return artist.lower() in _BLACK_LIST_ARTIST


VK_JENRE = {
    1: 'Rock',
    2: 'Pop',
    3: 'Rap & Hip-Hop',
    4: 'Easy Listening',
    5: 'Dance & House',
    6: 'Instrumental',
    7: 'Metal',
    21: 'Alternative',
    8: 'Dubstep',
    9: 'Jazz & Blues',
    10: 'Drum & Bass',
    11: 'Trance',
    12: 'Chanson',
    13: 'Ethnic',
    14: 'Acoustic & Vocal',
    15: 'Reggae',
    16: 'Classical',
    17: 'Indie Pop',
    19: 'Speech',
    22: 'Electropop & Disco',
    18: 'Other',
}


def popular_download(vk, genre_id, path_dir, count=1000):
    # Варианты значений data:
    #     only_eng	1 – возвращать только зарубежные аудиозаписи. 0 – возвращать все аудиозаписи. (по умолчанию)
    #     genre_id	идентификатор жанра из списка жанров (https://vk.com/dev/audio_genres)
    #     offset	смещение, необходимое для выборки определенного подмножества аудиозаписей.
    #     count	количество возвращаемых аудиозаписей (максимальное значение 1000, по умолчанию 100).
    data = {
        'genre_id': genre_id,
        'count': count,
    }

    try:
        list_audio = vk.method('audio.getPopular', data)
    except Exception as e:
        raise e

    # Если не существует пути, создадим его
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    downloads_count = 0
    filtered_audios = 0
    existing_audios = os.listdir(path_dir)

    print('Выбранный жанр "{}" (id={})'.format(VK_JENRE[genre_id], genre_id))
    print('Папка загрузки: "{}"'.format(os.path.abspath(path_dir)))
    print('Всего получено песен из запроса {}'.format(len(list_audio)))
    print()
    print('Начинаю скачиваение:')

    for i, audio in enumerate(list_audio, 1):
        try:
            url = audio['url']
            url, suffix = get_audio_url_info(url)

            # Убираем пробельные символы с начала и конца строк
            # В строке исполнителя: каждую первую букву слова в верхний регистр, остальные в нижний
            # В строке трека: первая буква первого слова в верхний регистр, остальные символы строки в нижний
            artist = audio['artist'].strip().title()
            title = audio['title'].strip().capitalize()

            if artist_in_black_list(artist):
                filtered_audios += 1
                raise Exception('Исполнитель "{}" в черном списке, пропускаем песню'.format(artist))

            name = '{} - {}{}'.format(artist, title, suffix)
            name = file_name_clear(name)

            if name in existing_audios:
                raise Exception('Пропускаем песню "{}" -- аудифайл уже существует'.format(name))

            print('{}. "{}"'.format(i, name), end='')

            # Путь в который будет скачен файл
            file_name = os.path.join(path_dir, name)

            download_file(url, file_name)
            make_pretty_id3(file_name, artist, title)
            downloads_count += 1
            existing_audios.append(name)
            print(' download finished...')

        except KeyboardInterrupt:
            print('\n\nСкачивание прервано.')
            sys.exit()

        except Exception as e:
            print('  audio id={} owner_id={}, error: {}'.format(audio['id'], audio['owner_id'], e))

    print()
    print('Скачалось песен {0}'.format(downloads_count))
    print('Всего пропущено песен {0} ({1:.0f}%)'.format(filtered_audios, filtered_audios / len(list_audio) * 100))
    print('\n')


LOGIN = ''
PASSWORD = ''
DOWNLOAD_DIR = 'popular downloads'


if __name__ == '__main__':
    print('Авторизация...')

    # Надоел Rammstein
    add_artist_to_black_list('Rammstein')

    try:
        vk = vk_api.VkApi(LOGIN, PASSWORD)
        vk.authorization()  # Авторизируемся

        # Закачиваем, например, на флешку:
        DOWNLOAD_DIR = 'G:'

        popular_download(vk, 7, os.path.join(DOWNLOAD_DIR, 'metal'))
        popular_download(vk, 1, os.path.join(DOWNLOAD_DIR, 'rock'))
        popular_download(vk, 21, os.path.join(DOWNLOAD_DIR, 'alternative'))
        popular_download(vk, 8, os.path.join(DOWNLOAD_DIR, 'dubstep'))

    except Exception as e:
        print('Error: ', e)
        sys.exit()
