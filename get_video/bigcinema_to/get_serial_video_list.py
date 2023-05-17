#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

import requests

from get_file_video_url import decode_base64_bigcinema_to


GET_PL_DATA_FROM_FLASHVALS_PATTERN = re.compile(r"""pl *?: *?['"](.+?)['"]""")


def get_video_list_url(url):
    rs = requests.get(url)
    if not rs.ok:
        return

    # Значений может быть несколько. И я не разобрался чем отличаются ссылки в file друг от друга,
    # поэтому берем первый попавшийся
    match = GET_PL_DATA_FROM_FLASHVALS_PATTERN.search(rs.text)
    if match is None:
        return

    pl_text_data_url = decode_base64_bigcinema_to(match.group(1))

    rs = requests.get(pl_text_data_url)
    if not rs.ok:
        return

    # Декодирование без поиска и замены мусора (секретного слова) -- мусора тут не было, а шанс удалить нужный
    # кусок есть
    data = decode_base64_bigcinema_to(rs.text, False)

    # Вернется json с описанием сезонов, их серий, а также для каждой серии будет доступно несколько ссылок на
    # файлы видео на разных серверах
    json_data = json.loads(data)
    return json_data


if __name__ == "__main__":
    url = "http://bigcinema.to/series/the-missing-mini-serial.html"
    print(get_video_list_url(url))

    url = "http://bigcinema.to/series/vse-shvacheno-serial-2016-man-with-a-plan.html"
    print(get_video_list_url(url))

    url = "http://bigcinema.to/series/kesem-sultan-dublyazh-muhtesem-yzyil-ksem.html"
    print(get_video_list_url(url))
