#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Вывод манг жанра 'game' с статусом 'Переведена'.

Скрипт авторизовывается на сайте grouple.ru, после идет на страницу закладок пользователя, там он
берет список url всех манг. После скрипт идет на страницу манг жанра 'game' и оттуда вытаскивает
список манг, у которых статус 'Переведена'.
В ходе поиска переведенных манг происходит вывод названия манги, включая локализованное название
(если оно есть), и путь к ней, а также происходит определение наличия манги в закладках, если манга
есть в закладках пользователя, выведется предупреждение.

Авторизация нужна только для получения закладок пользователя, чтобы можно было из них вытащить
список url манг.
Если не авторизовываться или авторизация прошла неудачно, то список переведенных манг жанра 'game'
будет все же получен, но не будет определения, если ли уже эта манга в закладках.
"""


from grab import Grab

LOGIN = ""
PASSWORD = ""

if __name__ == "__main__":
    g = Grab()

    # Авторизация
    g.go("http://grouple.ru/internal/auth/login")
    g.set_input("j_username", LOGIN)
    g.set_input("j_password", PASSWORD)
    g.submit()

    if g.response.url == "http://grouple.ru/internal/auth/login?login_error=1":
        print("Авторизация прошла неудачно :(")

    # Зайдем в закладки
    g.go("http://grouple.ru/private/bookmarks")

    # Получим список всех url'ов манг в закладках
    get_href_manga_xpath = '//div[@class="bookmarks-lists"]/*/tr/td/a/@href'
    all_bookmarks_href = [href.text() for href in g.doc.select(get_href_manga_xpath)]

    # Заходим на страницу жанра манг "игра"
    g.go("http://readmanga.me/list/genre/game")

    # Ищем элементы div, у которых есть дети div/span у которого есть класс "mangaTranslationCompleted",
    # и если мы такой нашли, мы у него ищем div с классом "desc"
    xpath = '//div[div/span[@class="mangaTranslationCompleted"]]/div[@class="desc"]'

    print("Список законченной и переведенной манги:")

    # Переберем список найденных элементов
    for i, tile in enumerate(g.doc.select(xpath), 1):
        title = tile.select("h3/a/@title").text()

        alt_title = tile.select("h4/@title")
        # Если альтернативный заголовок есть, добавим его
        if alt_title.count():
            title = f'"{title}" / "{alt_title.text()}"'
        else:
            title = f'"{title}"'

        href = "http://readmanga.me" + tile.select("h3/a/@href").text()

        if href not in all_bookmarks_href:
            print("{i}. {title}: {href}")
        else:
            print("Уже есть в закладках {title}: {href}")
