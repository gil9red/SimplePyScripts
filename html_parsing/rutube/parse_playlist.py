#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import logging
import re
import time
import sys

from dataclasses import dataclass
from typing import Any
from urllib.parse import ParseResult, urlparse, urlencode, parse_qsl

import requests


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/3377693e6b875394f0617a7c74fbd7fa834e1a0e/merge_url_params.py#L7-L17
def merge_url_params(url: str, params: dict) -> str:
    result: ParseResult = urlparse(url)

    current_params = dict(parse_qsl(result.query))
    merged_params = {**current_params, **params}

    new_query = urlencode(merged_params, doseq=True)
    return result._replace(query=new_query).geturl()


@dataclass
class Video:
    title: str
    url: str


logger = logging.getLogger("rutube-parser")
logger.setLevel(logging.WARNING)
default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)
logger.addHandler(default_handler)

session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/127.0"


def _get_playlist_videos(data: dict[str, Any]) -> dict[str, Any]:
    # Поиск ключа вида "getPlaylistVideos/<id плейлиста>"
    items: list[dict[str, Any]] = [
        v
        for k, v in data["api"]["queries"].items()
        if k.startswith("getPlaylistVideos")
    ]
    if not items or not items[0]:
        raise Exception("Не удалось найти getPlaylistVideos!")

    return items[0]


def _get_video_list(
    playlist_videos_data: dict[str, Any],
    playlist_id: int,
    page: int,
) -> list[Video]:
    results: list[dict] | None = playlist_videos_data["results"]
    if not results:
        return []

    return [
        Video(
            title=obj["title"],
            url=merge_url_params(
                obj["video_url"],
                {
                    "playlist": playlist_id,
                    "playlistPage": page,
                },
            ),
        )
        for obj in results
    ]


def _get_playlist_id(playlist_videos: dict[str, Any]) -> int:
    # NOTE: Еще можно получать из URL, но это кажется надежнее

    try:
        playlist_id = playlist_videos["originalArgs"]["playlistId"]
    except KeyError:
        raise Exception("Не удалось найти playlistId!")

    if not playlist_id:
        raise Exception("Пустое значение playlistId!")

    return playlist_id


def _get_page(playlist_videos_data: dict[str, Any]) -> int:
    try:
        page = playlist_videos_data["page"]
    except KeyError:
        raise Exception("Не удалось найти page!")

    if not page:
        raise Exception("Пустое значение page!")

    return page


def _get_next_page_url(playlist_videos_data: dict[str, Any]) -> str | None:
    return playlist_videos_data["next"]


def get_all_series(url: str, max_items: int | None = None) -> list[Video]:
    logger.info(f"Загрузка {url!r} (max_items: {max_items})")

    def _has_max_items(items: list[Video]) -> bool:
        return max_items is not None and len(items) >= max_items

    rs = session.get(url)
    rs.raise_for_status()

    # Первая порция данных находится в странице как объект js
    m = re.search(r"window\.reduxState\s*=\s*(\{.+});", rs.text)
    if not m:
        raise Exception('Не найдено "window.reduxState"!')

    # Подмена всяких "\x3d" на конкретные символы
    js_text = re.sub(
        r"\\x([0-9a-fA-F]{2})",
        lambda x: chr(int(x.group(1), 16)),
        m.group(1),
    )

    data: dict[str, Any] = json.loads(js_text)
    logger.debug(f"data: {data}")

    playlist_videos: dict[str, Any] = _get_playlist_videos(data)

    playlist_id: int = _get_playlist_id(playlist_videos)

    playlist_videos_data = playlist_videos["data"]
    page: int = _get_page(playlist_videos_data)
    logger.debug(f"playlist_id: {playlist_id}")
    logger.debug(f"page: {page}")

    items: list[Video] = _get_video_list(
        playlist_videos_data, playlist_id=playlist_id, page=page
    )
    logger.debug(f"items: {items}")

    # Последующие порции вытаскиваются отдельными запросами в API
    while True:
        next_page_url: str | None = _get_next_page_url(playlist_videos_data)
        logger.debug(f"next_page_url {next_page_url!r}")
        if not next_page_url:
            break

        logger.info(f"Загрузка {next_page_url!r}")

        rs = session.get(next_page_url)
        rs.raise_for_status()

        playlist_videos_data = rs.json()
        logger.debug(f"playlist_videos_data: {playlist_videos_data}")

        page: int = _get_page(playlist_videos_data)
        logger.debug(f"page: {page}")

        new_videos = _get_video_list(
            playlist_videos_data, playlist_id=playlist_id, page=page
        )
        logger.debug(f"new_videos: {new_videos}")
        if not new_videos:
            logger.info("Вернулся пустой список видео, завершение цикла")
            break

        items += new_videos
        if _has_max_items(items):
            break

        time.sleep(2)

    if _has_max_items(items):
        items = items[:max_items]

    return items


if __name__ == "__main__":
    items = get_all_series("https://rutube.ru/plst/337761/", max_items=10)
    assert len(items) == 10

    # NOTE: Для получения всех логов
    # logger.setLevel(logging.DEBUG)

    items = get_all_series("https://rutube.ru/plst/337761/")
    print(f"Video ({len(items)}):")
    for video in items:
        print(f"    {video.title!r}: {video.url}")
    """
    Video (32):
        'Пацаны 1 сезон 1 серия «Такая игра» (сериал, 2019)': https://rutube.ru/video/39a0a1f09bee6e956b60211d5b772963/?playlist=337761&playlistPage=1
        'Пацаны 1 сезон 2 серия «Вишенка» (сериал, 2019)': https://rutube.ru/video/1966bb2491b2cf241fae8934f164cff2/?playlist=337761&playlistPage=1
        'Пацаны 1 сезон 3 серия «Получи!» (сериал, 2019)': https://rutube.ru/video/aa130c541635000e6c93ac8d25e35146/?playlist=337761&playlistPage=1
        ...
        'Пацаны 4 сезон 6 серия «Грязный бизнес» (сериал, 2024)': https://rutube.ru/video/4c36deadf6e7d6fe93a9c3b9278049c2/?playlist=337761&playlistPage=2
        'Пацаны 4 сезон 7 серия «Инсайдер» (сериал, 2024)': https://rutube.ru/video/a7a667c6f66bfe1d2b83b4dd32b954b2/?playlist=337761&playlistPage=2
        'Пацаны 4 сезон 8 серия «Убийственный забег» (сериал, 2024)': https://rutube.ru/video/c5072e545c0cb21c3312c825f4c8b05a/?playlist=337761&playlistPage=2
    """

    # print()
    #
    # items = get_all_series("https://rutube.ru/plst/427058/")
    # print(f"Video ({len(items)}):")
    # for video in items:
    #     print(f"    {video.title!r}: {video.url}")
    # """
    # Video (182):
    #     'Клиника 1 сезон 1 серия «Мой первый день» (сериал, 2001-2010)': https://rutube.ru/video/4228bfef86749125f66a17c7a443d928/?playlist=427058&playlistPage=1
    #     'Клиника 1 сезон 2 серия «Мой наставник» (сериал, 2001-2010)': http://rutube.ru/video/9925af3696aaa73853e8a629293d7a19/?playlist=427058&playlistPage=1
    #     'Клиника 1 сезон 3 серия «Ошибка лучшего друга» (сериал, 2001-2010)': https://rutube.ru/video/52b4cc6ff8801a8c58329e68c14eecbb/?playlist=427058&playlistPage=1
    #     ...
    #     'Клиника 9 сезон 11 серия «Наши Дорогие Лидеры» (сериал, 2001-2010)': https://rutube.ru/video/195ff7bfba5760784c50fbb38f30f6c2/?playlist=427058&playlistPage=9
    #     'Клиника 9 сезон 12 серия «Наши Главные Проблемы» (сериал, 2001-2010)': https://rutube.ru/video/2e1184f3bde2da196547fd1c9e3e37ae/?playlist=427058&playlistPage=10
    #     'Клиника 9 сезон 13 серия «Наша Благодарность» (сериал, 2001-2010)': https://rutube.ru/video/899a93736642555bfd11b00cce3a4640/?playlist=427058&playlistPage=10
    # """
