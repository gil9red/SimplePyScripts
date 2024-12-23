#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Generator, Callable, Any
from urllib.parse import urljoin

from .common import (
    AlertError,
    BASE_URL,
    Video,
    Playlist,
    load,
    get_generator_raw_video_list_from_data,
)


def get_generator_raw_video_list(url: str) -> Generator[dict, None, None]:
    rs, data = load(url)
    yield from get_generator_raw_video_list_from_data(data, rs)


def get_raw_video_list(url: str, maximum_items: int = 1000) -> list[dict]:
    items = []
    for i, video in enumerate(get_generator_raw_video_list(url)):
        if i >= maximum_items:
            break

        items.append(video)

    return items


def get_video_list(url: str, *args, **kwargs) -> list[Video]:
    return [
        Video.parse_from(video)
        for video in get_raw_video_list(url, *args, **kwargs)
        if "videoId" in video  # NOTE: У плейлистов будет playlistId
    ]


def search_youtube(text_or_url: str, *args, **kwargs) -> list[Video]:
    if text_or_url.startswith("http"):
        url = text_or_url
    else:
        text = text_or_url
        url = urljoin(BASE_URL, f"results?search_query={text}")

    return get_video_list(url, *args, **kwargs)


def search_youtube_with_filter(
    url: str,
    sort: bool = False,
    filter_func: Callable[[Any], bool] = None,
) -> list[str]:
    video_title_list = [video.title for video in search_youtube(url)]
    if sort:
        video_title_list.sort()

    if callable(filter_func):
        video_title_list = list(filter(filter_func, video_title_list))

    return video_title_list
