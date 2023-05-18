#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


# Регулярка для вытаскивания id сериала из url
serial_id_from_url_pattern = re.compile(r"https?://seasonvar\.ru/serial-(\d+?)-")

# Регулярка для вытаскивания секретного случайного кода
secure_mark_pattern = re.compile(r'var secureMark = "(.*)";')


def get_video_list_url_from_seasonvar_ru(url):
    # url выглядят так: http://seasonvar.ru/serial-14590-Sofiya_Prekrasnaya-3-season.html
    # serial_id = serial_id_from_url_pattern.search(url)
    match = serial_id_from_url_pattern.search(url)
    if match is None:
        return

    serial_id = match.group(1)

    session = requests.session()

    rs = session.get(url)
    if not rs.ok:
        return

    match = secure_mark_pattern.search(rs.text)
    if match is None:
        return

    secure_mark = match.group(1)

    url_list_of_series = (
        f"http://seasonvar.ru/playls2/{secure_mark}x/trans/{serial_id}/list.xml"
    )
    rs = session.get(url_list_of_series)
    if not rs.ok:
        return

    list_of_series = list()

    # TODO: а разве бывают в seasonvar вложенные плейлисты?
    # TODO: Обработать название серии в comment -- удалить указания вариантов качества видео SD/HD и т.п.
    # указание перевода можно оставить, но нужно его также оформить
    # справа переводчик может быть и не указан (пример: сериал покемоны)
    for row in rs.json()["playlist"]:
        if "file" in row:
            list_of_series.append((row["comment"], row["file"]))

        elif "playlist" in row:
            for row2 in row["playlist"]:
                list_of_series.append((row2["comment"], row2["file"]))

    return list_of_series


if __name__ == "__main__":
    url = "http://seasonvar.ru/serial-14590-Sofiya_Prekrasnaya-3-season.html"
    print(get_video_list_url_from_seasonvar_ru(url))

    url = "http://seasonvar.ru/serial-4574-Gravity_Falls.html"
    print(get_video_list_url_from_seasonvar_ru(url))
