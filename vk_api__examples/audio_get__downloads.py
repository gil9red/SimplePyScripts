# !/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


"""
Download audio user
Скачивание аудиозаписей пользователя
"""


import os
import sys
from pathlib import Path

import requests

from vk_api.audio import VkAudio

# pip install mutagen
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.id3 import TIT2, TPE1

from root_common import get_vk_session


# https://github.com/python273/vk_api
# https://vk.com/dev/methods
# http://vk.com/dev/audio.getAlbums
# http://vk.com/dev/audio.get


# TODO: учитывать наличие разделения песен на альбомы
# TODO: возможность выбирать диапазоны индексов скачиваемых песен


def make_pretty_id3(audio_file_name: str, performer: str, title: str) -> None:
    """
    Функция удаляет из тега фреймы (COMM, PRIV, ...), добавляет (а если есть переписывает)
    фреймы TPE1 (имя группы) и TIT2 (название песни)

    """

    audio = ID3()

    try:
        audio.load(audio_file_name)

        album = audio.get("TALB")
        genre = audio.get("TCON")
        record_time = audio.get("TDRC")
        picture = audio.get("APIC")

        audio.delete()

        audio.add(TPE1(3, performer))
        audio.add(TIT2(3, title))

        if album:
            audio.add(album)

        if genre:
            audio.add(genre)

        if record_time:
            audio.add(record_time)

        if picture:
            audio.add(picture)

    except ID3NoHeaderError:
        audio.add(TPE1(3, performer))
        audio.add(TIT2(3, title))

    audio.save()


class DownloadFileError(Exception):
    pass


def file_name_clear(name: str) -> str:
    """Функция удаляет и заменяет символы, которые в имени
    файлов windows не могут быть

    """

    # TODO: Замена символов, которых в названиях файлов запрещено
    # Windows: \/:*?"<>|

    name = name.replace("\\", "-")
    name = name.replace("/", "-")
    name = name.replace(":", ".")
    name = name.replace("*", ".")
    name = name.replace("?", "")
    name = name.replace('"', "'")
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace("|", "")
    return name


def download_file(url: str, audio_file_name: str):
    # Попытаемся скачать аудиозапись
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Создаем файл и в него записываем файл с сервера
        with open(audio_file_name, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise DownloadFileError(
            f'Ошибка при скачивании "{url}": {r.status_code} - {r.reason}'
        )


DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = str(DIR / "downloads")


if __name__ == "__main__":
    print("Авторизация...\n")

    vk_session = get_vk_session()
    vk_audio = VkAudio(vk_session)

    audio_list = vk_audio.get()

    # Если не существует пути, создадим его
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Вывод списка всех аудиозаписей
    print(f"Всего песен: {len(audio_list)}")

    for i, audio in enumerate(audio_list, 1):
        try:
            artist = audio["artist"].strip().title()
            title = audio["title"].strip().capitalize()
            url = audio["url"]

            audio_name = f"{artist} - {title}"

            # Название файла аудиозаписи
            audio_file_name = audio_name + ".mp3"

            # Замена символов, которых в названиях файлов запрещено
            audio_file_name = file_name_clear(audio_file_name)

            # Путь в который будет скачен файл
            download_path = os.path.join(DOWNLOAD_DIR, audio_file_name)

            if os.path.exists(download_path):
                print(f"File is exist: {download_path}")
                continue

            print(f"{i}. {audio_name!r}", end="")
            download_file(url, download_path)
            make_pretty_id3(download_path, artist, title)
            print(" download finished...")

        except KeyboardInterrupt:
            print("\n\nСкачивание прервано.")
            sys.exit()

        except Exception as e:
            print(f'audio id={audio["id"]} owner_id={audio["owner_id"]}, error: {e}')
