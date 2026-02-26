#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def get_video_list(url) -> list[dict]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "lxml")

    pattern_get_duration = re.compile(r"(\d+).:(\d+).")

    items = []

    for item in root.select("#playlist_view_playlist_view_items > .item"):
        url = item.a["href"]
        title = item.a["title"]
        url_thumb = item.select_one("img")["src"]

        # Example: "60%", "80%"
        rating = item.select_one(".rating").text
        rating = int(rating.replace("%", ""))

        # Example: "0м:31с", "6м:32с"
        duration = item.select_one(".duration").text
        minutes, seconds = map(int, pattern_get_duration.findall(duration)[0])
        duration = minutes * 60 + seconds

        items.append({
            "title": title,
            "url": url,
            "duration": duration,
            "rating": rating,
            "url_thumb": url_thumb,
        })

    return items


if __name__ == "__main__":
    items = get_video_list("http://xcadr.com/collection/seks-v-poze-naezdnicy/")
    print("Total:", len(items))

    items = get_video_list("http://xcadr.com/collection/sceny-bdsm-v-filmah/")
    print("Total:", len(items))
    print()

    items = get_video_list("http://xcadr.com/collection/luchshie-sceny-v-bane/")
    print("Total:", len(items))

    def print_items(items) -> None:
        for i, item in enumerate(items, 1):
            print(
                '{0:2}. "{title}" ({duration} secs, rating: {rating}): {url} [{url_thumb}]'.format(
                    i, **item
                )
            )

    print("Sorted by duration (top 5):")
    new_items = sorted(items, key=lambda x: x["duration"], reverse=True)[:5]
    print_items(new_items)

    print()
    print("Sorted by duration:")
    new_items = sorted(items, key=lambda x: x["duration"], reverse=True)
    print_items(new_items)

    print()
    print("Sorted by rating:")
    new_items = sorted(items, key=lambda x: x["rating"], reverse=True)
    print_items(new_items)
