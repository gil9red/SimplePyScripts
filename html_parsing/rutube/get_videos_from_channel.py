#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from typing import Any

try:
    from .common import (
        Video,
        get_redux_state,
        logger,
        do_get,
        get_page,
        get_next_page_url,
    )
except ImportError:
    from common import (
        Video,
        get_redux_state,
        logger,
        do_get,
        get_page,
        get_next_page_url,
    )


def _get_channel_videos(data: dict[str, Any]) -> dict[str, Any]:
    try:
        try:
            result = data["userChannel"]["videos"]
        except KeyError:
            raise KeyError("Не удалось найти userChannel/videos!")

        if not result:
            raise KeyError("Пустое значение userChannel/videos!")

        return result

    except KeyError:
        try:
            # Поиск ключа вида "videos(<id канала>)"
            items: list[dict[str, Any]] = [
                v
                for k, v in data["api"]["queries"].items()
                if k.startswith("videos")
            ]
        except KeyError:
            raise KeyError("Не удалось найти api/queries!")

        if not items or not items[0]:
            raise KeyError("Не удалось найти api/queries/videos!")

        result: dict[str, Any] | None = items[0].get("data")
        if not result:
            raise KeyError("Пустое значение api/queries/videos/data!")

        return result


def _get_video_list(channel_videos_data: dict[str, Any]) -> list[Video]:
    results: list[dict] | None = channel_videos_data["results"]
    if not results:
        return []

    return [
        Video(
            title=obj["title"],
            url=obj["video_url"],
        )
        for obj in results
    ]


def get_videos(url: str, max_items: int | None = None) -> list[Video]:
    logger.info(f"Загрузка {url!r} (max_items: {max_items})")

    def _has_max_items(items: list[Video]) -> bool:
        return max_items is not None and len(items) >= max_items

    rs = do_get(url)
    data: dict[str, Any] = get_redux_state(rs.text)

    channel_videos_data: dict[str, Any] = _get_channel_videos(data)

    page: int = get_page(channel_videos_data)
    logger.debug(f"page: {page}")

    items: list[Video] = _get_video_list(channel_videos_data)
    logger.debug(f"items: {items}")

    # Последующие порции вытаскиваются отдельными запросами в API
    while True:
        next_page_url: str | None = get_next_page_url(channel_videos_data)
        logger.debug(f"next_page_url {next_page_url!r}")
        if not next_page_url:
            break

        logger.info(f"Загрузка {next_page_url!r}")

        rs = do_get(next_page_url)
        channel_videos_data = rs.json()
        logger.debug(f"channel_videos_data: {channel_videos_data}")

        page: int = get_page(channel_videos_data)
        logger.debug(f"page: {page}")

        new_videos = _get_video_list(channel_videos_data)
        logger.debug(f"new_videos: {new_videos}")
        if not new_videos:
            logger.info("Вернулся пустой список видео, завершение цикла")
            break

        for video in new_videos:
            if video not in items:
                items.append(video)

        if _has_max_items(items):
            break

        time.sleep(2)

    if _has_max_items(items):
        items = items[:max_items]

    return items


if __name__ == "__main__":
    # # NOTE: Для получения всех логов
    # import logging
    # logger.setLevel(logging.DEBUG)

    url = "https://rutube.ru/channel/32869212/videos/"
    items = get_videos(url, max_items=10)
    assert len(items) == 10

    items = get_videos(url, max_items=50)
    print(f"Video ({len(items)}):")
    for video in items:
        print(f"    {video.title!r}: {video.url}")
    """
    Video (50):
        'Игры джентльменов | The Ladykillers (2004)': https://rutube.ru/video/0fc7477fa6fb7ef167be5bdea70c1ffd/
        'Без глазури | Unfrosted (2024)': https://rutube.ru/video/730b9d06b1b83a53a663c969cffa735c/
        'Пиноккио | Pinocchio (2022)': https://rutube.ru/video/726f44bb8daaba912d4019c73b1b7269/
        ...
        'Крик 6 | Scream VI (2023)': https://rutube.ru/video/286aedeb8c88be6df7383cbefd91a3b4/
        'Особняк с привидениями | Haunted Mansion (2023)': https://rutube.ru/video/fe50e271927beb09edc846cdb09663c2/
        'Кокаиновый медведь | Cocaine Bear (2023)': https://rutube.ru/video/4c97fde96b97082aea94f5721f0d94fd/
    """

    # print()
    #
    # items = get_videos("https://rutube.ru/channel/32311072/videos/")
    # print(f"Video ({len(items)}):")
    # for video in items:
    #     print(f"    {video.title!r}: {video.url}")
    # """
    # Video (137):
    #     'Величайший император Китая / Золотой век Китайской империи / Уроки истории / МИНАЕВ': https://rutube.ru/video/bd72b967a81d88d3ce3ca0ff602b9e71/
    #     'Мексиканские картели / Криминальная история Мексики / Уроки истории / МИНАЕВ': https://rutube.ru/video/98bf4ed6a6afe5c3f14859d4eb12ae01/
    #     'ЖЕЛЕЗО: Как закалялась сталь / Простовещи / МИНАЕВ': https://rutube.ru/video/c35456b9d91f5813ad46f5fad4bbb619/
    #     ...
    #     'Великие пророки / Ванга, Нострадамус, Авель и Мессинг / Уроки истории / МИНАЕВ': https://rutube.ru/video/c8e4f0d42e9ba38a727e88f170bdf6e0/
    #     'Мао Цзэдун / Великий кормчий Китая / Личности / МИНАЕВ': https://rutube.ru/video/94266f52cf00228eee0e38b07a214887/
    #     'ХЛОПОК: История власти / Простовещи / МИНАЕВ': https://rutube.ru/video/56191ffd4b084ed4126c056036399f4e/
    # """
