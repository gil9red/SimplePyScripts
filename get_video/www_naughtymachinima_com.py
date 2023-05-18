#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


GET_VIDEO_ID_FROM_URL_PATTERN = re.compile(
    r"http://www\.naughtymachinima\.com/video/(\d+)/"
)


# TODO: голая ссылка на видео не работает, похоже без каких-то заголовков не получится скачать видео
# NOTE: интересен url: http://www.naughtymachinima.com/media/player/config.php?vkey=18317-1-1
#       в нем куча данных, включая ссылку на видео


def get_video_url(url):
    match = GET_VIDEO_ID_FROM_URL_PATTERN.search(url)
    if not match:
        return

    video_id = match.group(1)
    return "http://www.naughtymachinima.com/media/videos/iphone/{}.mp4".format(video_id)


if __name__ == "__main__":
    url = "http://www.naughtymachinima.com/video/18317/lara-with-horse-2-ep-4"
    video_url = get_video_url(url)
    print(video_url)
