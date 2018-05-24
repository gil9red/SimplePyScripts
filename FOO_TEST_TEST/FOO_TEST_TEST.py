#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


#  pip install Py-StackExchange
import stackexchange
from stackexchange.sites import __SEAPI

so = stackexchange.Site(__SEAPI('ru.stackoverflow.com'), impose_throttling=True)

from collections import OrderedDict
tag_by_wiki = OrderedDict()

page = 1

while True:
    for tag in so.all_tags(page=page):
        wiki = tag.wiki.fetch()
        print(tag.name, repr(wiki.excerpt))

    page += 1
    quit()

# print(so.all_tags()[0].name)
# print(so.all_tags(page=1)[0].name)
# print(so.all_tags(page=20000))
# quit()
# print(so.all_tags(page=20000)[0].name)
