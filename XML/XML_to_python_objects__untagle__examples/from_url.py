#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/stchris/untangle


# pip install untangle
# OR:
# pip install git+https://github.com/stchris/untangle.git
import untangle


obj = untangle.parse("https://news.yandex.ru/games.rss")
channel = obj.rss.channel
print(channel.title.cdata)  # Яндекс.Новости: Игры
print(channel.link.cdata)  # https://news.yandex.ru/games.html?from=rss
print(channel.image.url.cdata)  # https://company.yandex.ru/i/50x23.gif
print()

for item in channel.item:
    print(item.title.cdata, item.link.cdata)
