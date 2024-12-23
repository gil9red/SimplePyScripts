#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from api.common import Video, Playlist, AlertError
from api.search import (
    get_video_list,
    search_youtube,
    search_youtube_with_filter,
)


url_playlist = (
    "https://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r"
)


def __print_video_list(items: list[Video]):
    print(f"Items ({len(items)}):")
    for i, video in enumerate(items, 1):
        print(f"  {i:3}. {video.title!r}: {video.url}")


items = get_video_list(url_playlist)
__print_video_list(items)
"""
Items (226):
    1. 'Run freeCodeCamp Locally  (P8D2) - Live Coding with Jesse': https://www.youtube.com/watch?v=GFQ9VZYw2-0&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=1
    2. 'React Native Browser Editor  (P8D1) - Live Coding with Jesse': https://www.youtube.com/watch?v=drN9DEm3hFE&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=2
    3. 'React Native Web Styling Part 2  (P7D13) - Live Coding with Jesse': https://www.youtube.com/watch?v=VSLMJ2mZx5Y&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=3
    ...
  224. 'Material Design Cards - Live Coding with Jesse': https://www.youtube.com/watch?v=29ddZX4wjoE&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=224
  225. 'Building a Website: Team Page - Live Coding with Jesse': https://www.youtube.com/watch?v=pfgqJU1lG78&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=225
  226. 'Building a Website (P1D2) - Live Coding with Jesse': https://www.youtube.com/watch?v=rgYQ7nUulAQ&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=226
"""

print("\n" + "-" * 100 + "\n")

url_playlist = (
    "https://www.youtube.com/playlist?list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG"
)
items = search_youtube(url_playlist)
__print_video_list(items)
"""
Items (7):
    1. 'Intro to Java Programming - Course for Absolute Beginners': https://www.youtube.com/watch?v=GoXwIVyNvX0&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=1
    2. 'Functional Programming in Java - Full Course': https://www.youtube.com/watch?v=rPSL1alFIjI&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=2
    3. 'Spring Boot Tutorial for Beginners (Java Framework)': https://www.youtube.com/watch?v=vtPkZShrvXQ&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=3
    4. 'Learn Java 8 - Full Tutorial for Beginners': https://www.youtube.com/watch?v=grEKMHGYyns&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=4
    5. 'Data Structures Easy to Advanced Course - Full Tutorial from a Google Engineer': https://www.youtube.com/watch?v=RBSGKlAvoiM&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=5
    6. 'Spring Boot and Angular Tutorial - Build a Reddit Clone (Coding Project)': https://www.youtube.com/watch?v=DKlTBBuc32c&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=6
    7. 'Android Development for Beginners - Full Course': https://www.youtube.com/watch?v=fis26HvvDII&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=7
"""

print("\n" + "-" * 100 + "\n")

# Testing for: youtube, channel, channel videos
print(len(get_video_list("https://www.youtube.com/")))  # TODO: Под вопросом
print(len(get_video_list("https://www.youtube.com/c/TheBadComedian")))
print(len(get_video_list("https://www.youtube.com/c/TheBadComedian/videos")))
# 247
# 45
# 190

print("\n" + "-" * 100 + "\n")

is_live_now_video_list = [
    video for video in get_video_list("https://www.youtube.com/") if video.is_live_now
]
print(f"Is live now ({len(is_live_now_video_list)}):")
for i, video in enumerate(is_live_now_video_list, 1):
    print(f"{i}. {video.title!r}: {video.url}")

print("\n" + "-" * 100 + "\n")

items = search_youtube("щенки", maximum_items=25)
__print_video_list(items)
"""
Items (25):
    1. '🐾 Дружные мопсы - Серия 1 Сезон 1 - Мультфильмы Disney': https://www.youtube.com/watch?v=Eqyz-bFtkEM
    2. 'Лучшие Приколы про собак | Подборка приколов про собак и щенков #8': https://www.youtube.com/watch?v=wNqZM7e0_18
    3. 'СМЕШНЫЕ СОБАКИ И ЩЕНКИ 2020': https://www.youtube.com/watch?v=Grjk1K0YPSU
    ...
   23. 'Щенячий патруль и Мегащенки  Новые серии - 2021': https://www.youtube.com/watch?v=Gq63Zl0OL4k
   24. 'КАК ЩЕНКИ РАДУЮТСЯ МОЕМУ ПРИХОДУ АЛАБАЙ / КАК ЩЕНКИ АЛАБАЙ ЗАБАВНО БАЛУЮТСЯ': https://www.youtube.com/watch?v=QaMebbbCQ9E
   25. 'Макс и Катя играют с сюрпризами в огромных яйцах': https://www.youtube.com/watch?v=Mt7oS8Yq8YY
"""

print("\n" + "-" * 100 + "\n")

items = search_youtube(
    "https://www.youtube.com/results?search_query=slipknot official",
    maximum_items=50,
)
__print_video_list(items)
"""
Items (50):
    1. 'Knotfest Los Angeles 2021: On-Sale Now': https://www.youtube.com/watch?v=8ueHLoI8htY
    2. 'Joey Jordison: 1975 - 2021': https://www.youtube.com/watch?v=5hejcY2p4A4
    3. 'Knotfest Los Angeles: November 5, 2021 [TRAILER]': https://www.youtube.com/watch?v=9qXnhQ0p7FA
    ...
   48. 'Slipknot: Live at Download Festival 2019': https://www.youtube.com/watch?v=QO3j9niG1Og
   49. 'Slipknot - Orphan (Audio)': https://www.youtube.com/watch?v=dvLp3XPNAZ0
   50. 'Slipknot - Spit It Out [OFFICIAL VIDEO]': https://www.youtube.com/watch?v=ZPUZwriSX4M
"""

print("\n" + "-" * 100 + "\n")

url = "https://www.youtube.com/playlist?list=PLZfhqd1-Hl3DtfKRjleAWB-zYJ-pj7apK"
items = search_youtube_with_filter(url)
print(f"Items ({len(items)}): {items}")
# Items (3): ['История серии Diablo. Акт I', 'История серии Diablo. Акт II', 'История серии Diablo. Акт III']

print("\n" + "-" * 100 + "\n")

text = "Gorgeous Freeman -"
url = "https://www.youtube.com/user/antoine35DeLak/search?query=" + text
items = search_youtube_with_filter(url)
print(f"Items ({len(items)}): {items}")
# Items (46): ['Gorgeous Freeman - Episode 1 - The Suit', ..., 'The Epileptic Seizure [Gmod]']

items = search_youtube_with_filter(url, filter_func=lambda name: text in name)
print(f"Filtered items ({len(items)}): {items}")
# Filtered items (3): ['Gorgeous Freeman - Episode 1 - The Suit', 'Gorgeous Freeman - Episode 3 - The Part 1', 'Gorgeous Freeman - Episode 2 - The Crowbar']

print("\n" + "-" * 100 + "\n")

text = "Sally Face"
url = "https://www.youtube.com/user/HellYeahPlay/search?query=" + text
items = search_youtube_with_filter(url)
print(f"Items ({len(items)}): {items}")
# Items (244): ['ТВОРЕНИЯ ВЕЛЬЗЕВУЛА - Sally Face [ЭПИЗОД 4] #9', ..., 'ЛЕСБИЙСКИЙ ТРЭШНЯК - Love Is Strange']

items = search_youtube_with_filter(
    url, filter_func=lambda name: text in name and "эпизод" in name.lower()
)
print(f"Filtered items ({len(items)}): {items}")
# Filtered items (14): ['ТВОРЕНИЯ ВЕЛЬЗЕВУЛА - Sally Face [ЭПИЗОД 4] #9', ..., 'ПОИСК МЕРТВЫХ ЛЮДЕЙ ☠️ Sally Face [ЭПИЗОД 2] #4']

print("\n" + "-" * 100 + "\n")

# Test for MIX
try:
    url = "https://www.youtube.com/watch?v=QKEjrOIrCBI&list=RDQKEjrOIrCBI&start_radio=1"
    playlist = Playlist.get_from(url)
    print(playlist)
    print(len(playlist.video_list))
    __print_video_list(playlist.video_list)
except AlertError as e:
    print(f"Error: {str(e)!r} for {url}")
# Error: 'Этот тип плейлиста недоступен для просмотра.' for https://www.youtube.com/watch?v=QKEjrOIrCBI&list=RDQKEjrOIrCBI&start_radio=1
