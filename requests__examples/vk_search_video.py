#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт для эмуляции запроса поиска видео в vk"""


import json
import re

import requests


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"

if __name__ == "__main__":
    session = requests.Session()
    session.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"

    rs = session.get("https://m.vk.com")
    match = re.search(r'<form method="post" action="(.+?)"', rs.text)

    # Авторизация. По полученной ссылке делаем post запрос с данными формы -- логин и пароль
    url = match.group(1)
    url = url + "&email=" + LOGIN + "&pass=" + PASSWORD  # TODO: using params
    rs = session.post(url)

    rs = session.post(
        "https://vk.com/al_video.php?act=search_video&al=1&offset=0",
        data={"q": "Варкрафт 2016"},
    )
    print(rs)
    json_text = rs.text
    print(json_text)

    start = json_text.index("{")
    end = json_text.rindex("}")
    json_text = json_text[start : end + 1]
    print(json_text)

    data = json.loads(json_text)
    print(data)

    print()
    print("Result:")

    def get_video_file_urls(url):
        video_urls = list()

        rs = session.get(url)
        if not rs.ok:
            print(rs)
            return video_urls

        for source in re.findall(r"<source.+?>", rs.text):
            source = source.replace("\\", "")
            match = re.search('src="(http.+?\.mp4).*?"', source)
            if match:
                url_video = match.group(1)
                video_urls.append(url_video)

        return video_urls

    for video_data in data["list"]:
        print(video_data)
        owner = video_data[0]
        video_id = video_data[1]
        poster = video_data[2]
        title = video_data[3]

        # TODO: для мобильной ссылки работает поиск, однако качество всегдла -- 240
        # нужно научить парсер искать ссылки в другом формате, текущий -- через тег source работает
        video_url = "https://m.vk.com/video{}_{}".format(owner, video_id)
        print(title, video_url)
        for file_url in get_video_file_urls(video_url):
            print("    {}".format(file_url))
        print()
