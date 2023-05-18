#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://np1.github.io/pafy/
# https://github.com/mps-youtube/pafy
import pafy


def get_video_file_urls(url: str) -> list[dict]:
    video = pafy.new(url)

    file_url_list = []

    for s in video.streams:
        file_url_list.append({
            "url": s.url,
            "resolution": s.resolution,
            "extension": s.extension,
        })

    return file_url_list


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=lz4r-TtIOjA"
    print(get_video_file_urls(url))

    url = "https://www.youtube.com/watch?v=bMt47wvK6u0"
    print(get_video_file_urls(url))
