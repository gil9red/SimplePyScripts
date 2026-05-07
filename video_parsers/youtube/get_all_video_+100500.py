#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from api.common import Video
from api.search import search_youtube

MINIMUM_NUMBER: int = 500

TARGETS: list[tuple[str, str]] = [
    # ("Playlist", "https://www.youtube.com/playlist?list=PLC6A0625DCA9AAE2D"),
    ("Channel", "https://www.youtube.com/@adamthomasmoran/videos"),
]

problems: list[str] = []
for label, url in TARGETS:
    videos: list[Video] = search_youtube(url)
    count = len(videos)

    print(f"{label}: {count} videos")
    titles: list[str] = [f"{i}. {v}" for i, v in enumerate(videos, 1)]
    print(*titles[:5], sep="\n")
    print("...")
    print(*titles[-5:], sep="\n")

    print("\n" + "-" * 100 + "\n")

    if count <= MINIMUM_NUMBER:
        problems.append(f"{label} videos: expected > {MINIMUM_NUMBER}, got {count}")

if problems:
    raise Exception("\n".join(problems))
