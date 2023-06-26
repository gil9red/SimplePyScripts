#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import html
import feedparser


rss = feedparser.parse("http://bash.im/rss/")
print(rss.feed.subtitle)

for entry in rss.entries:
    quote = html.unescape(entry.summary)
    quote = quote.replace("<br>", "\n")

    print(f"{entry.title}: {entry.link}\n{quote}\n\n")
