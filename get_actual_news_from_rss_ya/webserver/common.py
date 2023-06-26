#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# # При выводе юникодных символов в консоль винды
# # Возможно, не только для винды, но и для любой платформы стоит использовать
# # эту настройку -- мало какие проблемы могут встретиться
# import sys
# if sys.platform == 'win32':
#     import codecs
#     sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
#     sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')


import sqlite3


DB_FILE_NAME = "database.sqlite"


def create_connect():
    return sqlite3.connect(DB_FILE_NAME)


def init_db():
    # Создание базы и таблицы
    connect = create_connect()
    try:
        connect.executescript(
            """
            CREATE TABLE IF NOT EXISTS News (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                interest TEXT NOT NULL,
                is_read BOOLEAN NOT NULL DEFAULT 0,

                CONSTRAINT news_url_unique UNIQUE (url)
            );
        """
        )

        connect.commit()

        # NOTE: Пример, когда нужно в таблице подправить схему:
        # cursor.executescript('''
        # DROP TABLE Game2;
        #
        # CREATE TABLE IF NOT EXISTS Game2 (
        #     id INTEGER PRIMARY KEY,
        #
        #     name TEXT NOT NULL,
        #     price TEXT DEFAULT NULL,
        #     modify_date TIMESTAMP DEFAULT NULL,
        #     kind TEXT NOT NULL,
        #     check_steam BOOLEAN NOT NULL DEFAULT 0
        # );
        #
        # INSERT INTO Game2 SELECT * FROM Game;
        #
        # DROP TABLE Game;
        # ALTER TABLE Game2 RENAME TO Game;
        #
        # ''')
        #
        # connect.commit()

    finally:
        connect.close()


def append_list_news(list_news: [str, str], interest: str):
    connect = create_connect()

    def insert_news(title, url, interest):
        # Для отсеивания дубликатов
        has = connect.execute("SELECT 1 FROM News WHERE url = ?", (url,)).fetchone()
        if has:
            return

        print(f'Добавляю новость "{title}" ({interest})')
        connect.execute(
            "INSERT OR IGNORE INTO News (title, url, interest) VALUES (?,?,?)",
            (title, url, interest),
        )

    try:
        for title, url in list_news:
            insert_news(title, url, interest)

        connect.commit()

    finally:
        connect.close()


def get_news_list(interest: str = None, last: int = None) -> ([str, str, str], int):
    connect = create_connect()

    try:
        if interest:
            news_list = connect.execute(
                "SELECT title, url, interest from News where interest = ?", (interest,)
            ).fetchall()
        else:
            news_list = connect.execute(
                "SELECT title, url, interest from News"
            ).fetchall()

        total = len(news_list)

        # TODO: лучше вытаскивать из базы последние <last> записей чем так
        if last and last != -1:
            news_list = news_list[-last:]

        return news_list, total

    finally:
        connect.close()


def get_news_list_and_mark_as_read(
    interest: str = None, count: int = None
) -> ([str, str, str], int):
    connect = create_connect()

    try:
        if interest:
            news_list = connect.execute(
                "SELECT id, title, url, interest from News where interest = ? and is_read = 0",
                (interest,),
            ).fetchall()
        else:
            news_list = connect.execute(
                "SELECT id, title, url, interest from News where is_read = 0"
            ).fetchall()

        # Всего непрочитанных новостей
        total = len(news_list)

        # TODO: лучше вытаскивать из базы <count> записей чем так
        if count and count != -1:
            news_list = news_list[:count]

        # Осталось непрочитанных новостей
        total -= len(news_list)

        # Устанавливаем новостям флаг того что они прочитаны
        for _id, _, _, interest in news_list:
            connect.execute("UPDATE News SET is_read = 1 WHERE id = ?", (_id,))

        connect.commit()

        return [
            (title, url, interest) for _id, title, url, interest in news_list
        ], total

    finally:
        connect.close()


def reset_all_is_read():
    connect = create_connect()

    try:
        connect.execute("UPDATE News SET is_read = 0")
        connect.commit()

    finally:
        connect.close()
