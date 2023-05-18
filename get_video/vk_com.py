#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def get_video_file_urls(url):
    video_urls = list()

    rs = requests.get(url)
    if not rs.ok:
        return video_urls

    for source in re.findall(r"<source.+?>", rs.text):
        source = source.replace("\\", "")
        match = re.search(r'src="(http.+?\.mp4).*?"', source)
        if match:
            url_video = match.group(1)
            video_urls.append(url_video)

    return video_urls


if __name__ == "__main__":
    # Пишет: Страница доступна только авторизованным пользователям.
    # ['https://cs514210.vk.me/u80746722/videos/bb238dead1.240.mp4']
    print(get_video_file_urls("https://m.vk.com/video80746722_163361560"))

    # ['https://cs514210.vk.me/u80746722/videos/bb238dead1.360.mp4', 'https://cs514210.vk.me/u80746722/videos/bb238dead1.240.mp4']
    print(get_video_file_urls("https://vk.com/video80746722_163361560"))

    # ['https://cs508203.vk.me/4/u94788893/videos/1119e2d5ca.720.mp4', 'https://cs3-1v4.vk-cdn.net/p6/8e6972dc8e27.480.mp4', 'https://cs508202.vk.me/4/u94788893/videos/1119e2d5ca.360.mp4', 'https://cs508202.vk.me/4/u94788893/videos/1119e2d5ca.240.mp4']
    print(get_video_file_urls("https://vk.com/video-47366412_171735915"))

    # TODO: нет доступа, нужно с подобным разобраться
    print(get_video_file_urls("https://vk.com/video-121893751_456239017"))
    print(get_video_file_urls("https://m.vk.com/video-121893751_456239017"))
