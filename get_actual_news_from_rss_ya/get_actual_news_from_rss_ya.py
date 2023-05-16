#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import feedparser


def get_news() -> list:
    rss = feedparser.parse("https://news.yandex.ru/games.rss")
    return [(entry.title, entry.id) for entry in rss.entries]


if __name__ == "__main__":
    import time

    current_news = []

    while True:
        new_feeds = get_news()
        print(len(new_feeds), [title for title, _ in new_feeds])
        # print(new_feeds)

        # Проверка что какие-то новости уже есть
        if current_news:
            news = set(new_feeds) - set(current_news)
            if news:
                current_news = new_feeds

                for title, _id in news:
                    print(title)

                print()

        else:
            current_news = new_feeds

        # Every 5 minutes
        time.sleep(60 * 5)
