__author__ = 'ipetrash'

# Скрипт качает цитаты Конфуция из викицитатника.

from grab import Grab


def get_confucius_quotes():
    g = Grab()
    # http://ru.wikiquote.org/wiki/Конфуций
    url = "http://ru.wikiquote.org/wiki/%D0%9A%D0%BE%D0%BD%D1%84%D1%83%D1%86%D0%B8%D0%B9"
    g.go(url)

    quotes = list()
    for el in g.doc.select('//h2/following-sibling::ul/li'):
        quotes.append(el.text())

    return quotes


if __name__ == '__main__':
    for q in get_confucius_quotes():
        print("'{}'".format(q))