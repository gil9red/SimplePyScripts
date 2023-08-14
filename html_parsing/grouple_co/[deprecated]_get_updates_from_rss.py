#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install feedparser==6.0.8
import feedparser


URL_USER_RSS = "https://grouple.co/user/rss/315828?filter="
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
)


def get_feeds_by_manga_chapters(url: str = URL_USER_RSS) -> list[str]:
    feed = feedparser.parse(url, agent=USER_AGENT)

    feeds = []
    for entry in feed.entries:
        title: str = entry.title
        title = (
            title.replace("&quot;", '"')
            .replace("Манга", "")
            .replace("Взрослая манга", "")
            .strip()
        )

        feeds.append(title)

    return feeds


if __name__ == "__main__":
    items = get_feeds_by_manga_chapters()
    print(f"Items ({len(items)}):", items)
