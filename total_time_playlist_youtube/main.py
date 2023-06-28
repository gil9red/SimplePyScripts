#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

sys.path.append("../html_parsing")
from youtube_com__results_search_query import Playlist


def parse_playlist_time(url_or_id: str) -> tuple[str, int, list[tuple[str, str]]]:
    """Функция парсит страницу плейлиста и подсчитывает сумму продолжительности роликов."""

    playlist = Playlist.get_from(url_or_id)
    items = [(video.title, video.duration_text) for video in playlist.video_list]
    return playlist.title, playlist.duration_seconds, playlist.duration_text, items


if __name__ == "__main__":
    url = "https://www.youtube.com/playlist?list=PLndO6DOY2cLyxQYX7pkDspTJ42JWx07AO"

    title, total_seconds, total_seconds_text, items = parse_playlist_time(url)

    print(f"Playlist {title!r}:")
    for i, (title, time) in enumerate(items, 1):
        print(f"  {i}. {title!r} ({time})")

    print()
    print(f"Total time: {total_seconds_text} ({total_seconds} total seconds)")

    """
    Playlist 'Dark Souls':
      1. 'Горит от чатика - Dark Souls #1' (06:41:58)
      2. 'Нашествие Альтруистов - Dark Souls #2' (05:26:41)
      3. 'ГОРИТ ОЧАГ - Dark Souls #3' (07:53:18)
      4. 'БОЛЬШЕ ТУПЫХ СОВЕТОВ - Dark Souls #4' (08:27:04)
      5. 'ДА НАЧНЕТСЯ ГОРЕНИЕ - Dark Souls #5' (07:12:00)
      6. 'ЖАРЬ СОСИСКИ НА МОЕМ ПЕРДАКЕ - Dark Souls #6' (06:34:32)
      7. 'НАКОНЕЦ-ТО! - Dark Souls #7 [ФИНАЛ]' (07:35:55)
    
    Total time: 49:51:28 (179488 total seconds)
    """
