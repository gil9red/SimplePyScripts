# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys
import urllib.parse

from audio_get__downloads import DIR, VkAudio, get_vk_session, file_name_clear, download_file, make_pretty_id3


# Список исполнителей, песни которых не хотим качать
_BLACK_LIST_ARTIST = []


def add_artist_to_black_list(artist):
    """Функция добавляет исполнителя в черный список."""
    _BLACK_LIST_ARTIST.append(artist.lower())


def artist_in_black_list(artist):
    """Функция вернет True, если исполнитель в черном списке."""
    return artist.lower() in _BLACK_LIST_ARTIST


DOWNLOAD_DIR = str(DIR / 'popular downloads')


if __name__ == '__main__':
    print('Авторизация...\n')

    vk_session = get_vk_session()
    vk_audio = VkAudio(vk_session)

    # Пропускаем
    add_artist_to_black_list('Coldplay')
    add_artist_to_black_list('Vesna305')

    # Если не существует пути, создадим его
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filtered_audios = 0
    downloads_count = 0

    count = 15
    for i, audio in enumerate(vk_audio.get_news_iter(), 1):
        if i > count:
            break

        try:
            url = audio['url']

            # Убираем пробельные символы с начала и конца строк
            # В строке исполнителя: каждую первую букву слова в верхний регистр, остальные в нижний
            # В строке трека: первая буква первого слова в верхний регистр, остальные символы строки в нижний
            artist = audio['artist'].strip().title()
            title = audio['title'].strip().capitalize()

            if artist_in_black_list(artist):
                filtered_audios += 1
                raise Exception(f'Исполнитель "{artist}" в черном списке, пропускаем песню')

            name = f'{artist} - {title}.mp3'
            name = file_name_clear(name)

            # Путь в который будет скачен файл
            file_name = os.path.join(DOWNLOAD_DIR, name)

            if os.path.exists(file_name):
                raise Exception(f'Пропускаем песню {name!r} - аудиофайл уже существует')

            print(f'{i}. {name!r}', end='')
            download_file(url, file_name)
            make_pretty_id3(file_name, artist, title)
            downloads_count += 1
            print(' download finished...')

        except KeyboardInterrupt:
            print('\n\nСкачивание прервано.')
            sys.exit()

        except Exception as e:
            print(f'  audio id={audio["id"]} owner_id={audio["owner_id"]}, error: {e}')
            continue

    print()
    print(f'Скачалось песен {downloads_count}')
    print(f'Всего пропущено песен {filtered_audios} ({filtered_audios / i * 100:.0f}%)')
