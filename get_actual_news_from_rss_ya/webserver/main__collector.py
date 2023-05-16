#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import feedparser

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
import sys
sys.path.append("../../wait")
from wait import wait


def get_news_from_rss(url_rss) -> list:
    rss = feedparser.parse(url_rss)
    return [(entry.title, entry.link) for entry in rss.entries]


if __name__ == "__main__":
    import time
    import traceback

    from common import *

    init_db()

    while True:
        try:
            news_from_games = get_news_from_rss("https://news.yandex.ru/games.rss")
            print("games", news_from_games)
            append_list_news(news_from_games, interest="games")

            news_from_movies = get_news_from_rss("https://news.yandex.ru/movies.rss")
            print("movies", news_from_movies)
            append_list_news(news_from_movies, interest="movies")

            wait(minutes=4)

        except Exception:
            print("Ошибка:")
            print(traceback.format_exc())

            print("Через 5 минут попробую снова...")

            # Wait 5 minutes before next attempt
            time.sleep(5 * 60)

    # news_list = get_news_list_and_mark_as_read(interest='games')
    # print(news_list)
    #
    # connect = create_connect()
    # news_list = connect.execute("SELECT * from News").fetchall()
    # print(news_list)

    # from common import create_connect
    #
    # news = get_news('https://news.yandex.ru/games.rss')  # movies
    # print(news)
    #
    # for title, url in news:
    #     # Создание базы и таблицы
    #     connect = create_connect()
    #
    #     interest = 'games'
    #     news_list = connect.execute("SELECT * from News where interest = ?", (interest, )).fetchall()
    #     print(news_list)
    #     quit()
    #
    #     try:
    #         interest = 'games'
    #
    #         connect.execute("INSERT OR IGNORE INTO News (title, url, interest) VALUES (?,?,?)", (title, url, interest))
    #         connect.commit()
    #
    #     finally:
    #         connect.close()

    sys.exit()

    while True:
        try:
            # Перед выполнением, запоминаем дату и время, чтобы иметь потом представление когда
            # в последний раз выполнялось заполнение списка
            from datetime import datetime

            today = datetime.today()
            print(today)

            # Every 5 minutes
            wait(minutes=5)

        except Exception:
            import traceback

            print("Ошибка:")
            print(traceback.format_exc())

            print("Через 5 минут попробую снова...")

            # Wait 5 minutes before next attempt
            import time

            time.sleep(5 * 60)
