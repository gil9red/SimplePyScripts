#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import random
import re

import requests


url_serial_name_from_url = re.compile(r"http://kinogo\.club/\d+?-(.+?)\.html")


def get_video_list_url_from_seasonvar_ru(url):
    match = url_serial_name_from_url.search(url)
    if match is None:
        return

    serial_url_name = match.group(1)

    # Пример: http://kinogo.club/playlist/sklifosovskiy-3-sezon.txt?rand=0.24304015329107642
    get_playlist_url = f"http://kinogo.club/playlist/{serial_url_name}.txt?rand={random.random()}"

    rs = requests.get(get_playlist_url)
    if not rs.ok:
        return

    # Небольшое ухищрение. В начале json приходит набор символов "п»ї" и они мешают парсеру JSON.
    json_data = json.loads(rs.text[3:])

    list_of_series = list()

    for row in json_data["playlist"]:
        if "file" in row:
            list_of_series.append(
                (row["comment"].encode("cp1251").decode("utf-8"), row["file"])
            )

    return list_of_series


if __name__ == "__main__":
    url = "http://kinogo.club/6583-simpsony-28-sezon.html"
    print(get_video_list_url_from_seasonvar_ru(url))

    url = "http://kinogo.club/4733-sklifosovskiy-3-sezon.html"
    print(get_video_list_url_from_seasonvar_ru(url))
