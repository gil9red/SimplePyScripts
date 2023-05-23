#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def secure_filename(text: str) -> str:
    return re.sub(r"[^\w .]", "", text).strip()


def download(dir_video: Path, url: str):
    session = requests.session()
    session.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"

    rs = session.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    for a in reversed(root.select(".caption > a[href]")):
        url_video = urljoin(rs.url, a["href"])
        title_file_name = secure_filename(a.text)
        print(url_video)

        rs = session.get(url_video)
        root = BeautifulSoup(rs.content, "html.parser")
        video_player = root.select_one(".video-player[data-preroll-file]")

        # Example: "[360p]https://d1.stopgame.ru/video.360p/gildiya_6_y_sezon_epizod_12_zavershenie_igry.stopgame.ru.1462106534.360p.mp4,[480p]https://d1.stopgame.ru/video.480p/gildiya_6_y_sezon_epizod_12_zavershenie_igry.stopgame.ru.1462106534.480p.mp4,[720p]https://d1.stopgame.ru/video.720p/gildiya_6_y_sezon_epizod_12_zavershenie_igry.stopgame.ru.1462106534.720p.mp4"
        data_preroll_file = video_player["data-preroll-file"]

        # Example: "https://d1.stopgame.ru/video.720p/gildiya_6_y_sezon_epizod_12_zavershenie_igry.stopgame.ru.1462106534.720p.mp4"
        url_mp4 = data_preroll_file.split(",")[-1].split("]")[1]
        suffix = url_mp4.split(".")[-1]

        file_name = dir_video / f"{title_file_name}.{suffix}"
        if file_name.exists():
            print("The video has already been downloaded! Skip!")
            continue

        print(f"Download video {url_mp4}")
        rs_video = session.get(url_mp4, stream=True)
        with open(file_name, mode="wb") as f:
            for data in rs_video.iter_content(chunk_size=1024):
                f.write(data)

        print(f"Download video {url_mp4} finished")
        print()
