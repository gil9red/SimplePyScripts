#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://np1.github.io/pafy/
# https://github.com/mps-youtube/pafy
import pafy


video = pafy.new("https://www.youtube.com/watch?v=lz4r-TtIOjA")

print(video.title)
print(video.rating)
print(video.viewcount, video.author, video.length)
print(video.duration, video.likes, video.dislikes)

streams = video.streams
for s in streams:
    print(s, s.resolution, s.extension, s.get_filesize(), s.url)
