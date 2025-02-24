#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import re
import shutil
import sys

from pathlib import Path

from bs4 import BeautifulSoup
import requests

sys.path.append(str(Path(__file__).parent.parent.parent))
from human_byte_size import sizeof_fmt


default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)
logger = logging.getLogger("jut.su-parser")
logger.setLevel(logging.WARNING)
logger.addHandler(default_handler)

session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"


def download_video(
    url: str,
    download_dir: Path | None = None,
) -> Path:
    logger.debug(f"Url: {url}")

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    title: str = (
        soup.select_one(".header_video > [itemprop=name]")
        or soup.select_one(".video_h > [itemprop=name]")
    ).get_text(strip=True)

    description: str = (
        soup.select_one('.header_video[itemprop="description"]')
        or soup.select_one(".video_plate_title > span > h2")
    ).get_text(strip=True)

    title = f"{title} - {description}"
    logger.debug(f"Title: {title}")

    title = re.sub("Смотреть", "", title, flags=re.IGNORECASE)
    title = re.sub(r"[^\w _.-]", " ", title)
    title = re.sub(" {2,}", " ", title)
    title = title.strip()
    logger.debug(f"Title [processed]: {title}")

    items = [
        (int(src["res"]), src["type"].split("/")[-1], src["src"])
        for src in soup.select("#my-player > source[src][res][type]")
    ]

    res, video_type, video_url = max(items, key=lambda x: x[0])
    logger.debug(f"Selected: res={res}, video_type={video_type}, video_url={video_url}")

    file_name: Path = Path(f"{title}.{video_type}")
    if download_dir:
        download_dir.mkdir(parents=True, exist_ok=True)

        file_name = download_dir / file_name

    file_name = file_name.absolute()

    logger.info(f"Download to: {file_name}")

    with session.get(video_url, stream=True) as r:
        r.raise_for_status()

        with open(file_name, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    logger.info(f"Finished! File size: {sizeof_fmt(file_name.stat().st_size)}")

    return file_name


if __name__ == "__main__":
    # NOTE: Для получения всех логов
    logger.setLevel(logging.DEBUG)

    download_dir: Path = Path(__file__).parent / "out"

    for url in [
        "https://jut.su/deshi-kenichi/episode-6.html",
        "https://jut.su/deshi-kenichi/episode-10.html",
        "https://jut.su/naruuto/season-1/episode-136.html",
        "https://jut.su/naruuto/season-2/episode-274.html",
    ]:
        file_name: Path = download_video(url, download_dir)
        print(file_name)
