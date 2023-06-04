#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

# pip install pytube3 --upgrade
from pytube import YouTube


url = "https://www.youtube.com/watch?v=90KZnwrVMgY"

yt = YouTube(url)
print(f"Download video {yt.title!r}: {url}")

# Атрибут progressive=True нужен, чтобы получить поток с видео и аудио в одном файле
streams = yt.streams.filter(
    progressive=True, file_extension="mp4", resolution="720p"
).order_by("resolution")

if not streams:
    print("Not found mp4 with 720p!")
    sys.exit()

video = streams[-1]
print("Stream url:", video.url)
video.download()
