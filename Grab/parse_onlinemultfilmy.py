#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Поиск мультсериалов 16+
# Пример сериала: 'http://onlinemultfilmy.ru/bratya-ventura/'


import time
from grab import Grab


g = Grab()

# TODO: магическое число нужно заменить
# Перебор страниц с мультами
for i in range(1, 82 + 1):
    url_page = f"http://onlinemultfilmy.ru/multserialy/page/{i}"
    print(url_page)

    # Загрузка страницы с мультами
    g.go(url_page)

    # Перебор и загрузка мультов на странице
    for url in g.doc.select('//div[@class="cat-post"]/a'):
        g.go(url.attr("href"))

        if g.doc.select('//*[@class="age_icon age_icon_16"]').count():
            print("    ", url.attr("title"), url.attr("href"))

        # Чтобы сервер не посчитал это дос атакой
        time.sleep(2)
