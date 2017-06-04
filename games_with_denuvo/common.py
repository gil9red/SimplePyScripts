#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# # TODO: костыль для винды, для исправления проблем с исключениями
# # при выводе юникодных символов в консоль винды
# # Возможно, не только для винды, но и для любой платформы стоит использовать
# # эту настройку -- мало какие проблемы могут встретиться
# import sys
# if sys.platform == 'win32':
#     import codecs
#     sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
#     sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')


from config import *


def get_logger(name, file='log.txt', encoding='utf8'):
    import sys
    import logging

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


log = get_logger('games_with_denuvo')
log_cracked_games = get_logger('cracked_games', file='cracked_games.log.txt')


def send_sms(api_id: str, to: str, text: str):
    log.debug('Отправка sms: "%s"', text)

    try:
        # Отправляю смс на номер
        url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
            api_id=api_id,
            to=to,
            text=text
        )
        log.debug(repr(url))

        import requests
        rs = requests.get(url)
        log.debug(repr(rs.text))

    except Exception:
        log.exception("При отправке sms произошла ошибка:")


DB_FILE_NAME = 'database.sqlite'


def create_connect():
    import sqlite3
    return sqlite3.connect(DB_FILE_NAME)


def init_db():
    # Создание базы и таблицы
    connect = create_connect()
    try:
        connect.execute('''
            CREATE TABLE IF NOT EXISTS Game (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                is_cracked BOOLEAN NOT NULL,

                CONSTRAINT name_unique UNIQUE (name)
            );
        ''')

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


def append_list_games(games: [(str, bool)], notified_by_sms=True):
    connect = create_connect()

    def insert(name: str, is_cracked: bool) -> bool:
        # Для отсеивания дубликатов
        has = connect.execute("SELECT 1 FROM Game WHERE name = ?", (name,)).fetchone()
        if has:
            return False

        log.debug('Добавляю "%s" (%s)', name, is_cracked)
        connect.execute("INSERT OR IGNORE INTO Game (name, is_cracked) VALUES (?,?)", (name, is_cracked))

        return True

    try:
        for name, is_cracked in games:
            ok = insert(name, is_cracked)

            # Игра уже есть в базе, нужно проверить ее статус is_cracked,  возможно, он поменялся и игру взломали
            if not ok:
                rs_is_cracked = connect.execute('SELECT is_cracked FROM Game where name = ?', (name,)).fetchone()[0]

                # Если игра раньше имела статус is_cracked = False, а теперь он поменялся на True:
                if not rs_is_cracked and is_cracked:
                    # Поменяем флаг у игры в базе
                    connect.execute('UPDATE Game SET is_cracked = 1 WHERE name = ?', (name,))

                    text = 'Игру "{}" взломали'.format(name)
                    log.debug(text)
                    log_cracked_games.debug(text)

                    if notified_by_sms:
                        send_sms(API_ID, TO, text)

            elif is_cracked:
                text = 'Добавлена взломанная игра "{}"'.format(name)
                log.debug(text)
                log_cracked_games.debug(text)

                if notified_by_sms:
                    send_sms(API_ID, TO, text)

        connect.commit()

    finally:
        connect.close()


def get_games(filter_by_is_cracked=None, sorted_by_name=True) -> [(str, bool)]:
    connect = create_connect()

    try:
        if filter_by_is_cracked is None:
            items = connect.execute("SELECT name, is_cracked FROM Game").fetchall()
        else:
            items = connect.execute("SELECT name, is_cracked FROM Game WHERE is_cracked = ?", (filter_by_is_cracked,)).fetchall()

        if sorted_by_name:
            items.sort(key=lambda x: x[0])

        return items

    finally:
        connect.close()


if __name__ == '__main__':
    games = get_games()
    print('Games:', len(games), games)

    games = get_games(filter_by_is_cracked=True)
    print('Cracked:', len(games), [name for name, _ in games])

    games = get_games(filter_by_is_cracked=False)
    print('Not cracked:', len(games), [name for name, _ in games])
