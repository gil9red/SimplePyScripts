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


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        import sys
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


DEBUG = False


if DEBUG:
    DB_FILE_NAME = 'test.database.sqlite'

    log = get_logger('test_games_with_denuvo', file='test_log.txt')
    log_cracked_games = get_logger('test_cracked_games', file='test_cracked_games.log.txt', log_stdout=False)

else:
    DB_FILE_NAME = 'database.sqlite'

    log = get_logger('games_with_denuvo')
    log_cracked_games = get_logger('cracked_games', file='cracked_games.log.txt', log_stdout=False)


def send_sms(api_id: str, to: str, text: str):
    log.info('Отправка sms: "%s"', text)

    # Отправляю смс на номер
    url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
        api_id=api_id,
        to=to,
        text=text
    )
    log.debug(repr(url))

    while True:
        try:
            import requests
            rs = requests.get(url)
            log.debug(repr(rs.text))

            break

        except:
            log.exception("При отправке sms произошла ошибка:")
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)


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
                crack_date TIMESTAMP DEFAULT NULL,

                CONSTRAINT name_unique UNIQUE (name)
            );
        ''')

        # # NOTE: Пример, когда нужно в таблице подправить схему:
        # connect.executescript('''
        #     DROP TABLE IF EXISTS Game2;
        #
        #     CREATE TABLE IF NOT EXISTS Game2 (
        #         id INTEGER PRIMARY KEY,
        #         name TEXT NOT NULL,
        #         is_cracked BOOLEAN NOT NULL,
        #         crack_date TIMESTAMP DEFAULT NULL,
        #
        #         CONSTRAINT name_unique UNIQUE (name)
        #     );
        #
        #     INSERT INTO Game2 SELECT id, name, is_cracked, date('now') FROM Game;
        #
        #     DROP TABLE Game;
        #     ALTER TABLE Game2 RENAME TO Game;
        # ''')

        connect.commit()

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

        # Если добавлена уже взломанная игра, указываем дату
        if is_cracked:
            connect.execute("UPDATE Game SET crack_date = date('now') WHERE name = ?", (name,))

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
                    connect.execute("UPDATE Game SET is_cracked = 1, crack_date = date('now') WHERE name = ?", (name,))

                    text = 'Игру "{}" взломали'.format(name)
                    log.info(text)
                    log_cracked_games.debug(text)

                    # При DEBUG = True, отправки смс не будет
                    if notified_by_sms and not DEBUG:
                        send_sms(API_ID, TO, text)

            elif is_cracked:
                text = 'Добавлена взломанная игра "{}"'.format(name)
                log.info(text)
                log_cracked_games.debug(text)

                # При DEBUG = True, отправки смс не будет
                if notified_by_sms and not DEBUG:
                    send_sms(API_ID, TO, text)

        connect.commit()

    finally:
        connect.close()


def get_games(filter_by_is_cracked=None, sorted_by_name=True, sorted_by_crack_date=False) -> [(str, bool, str)]:
    """
    Функция возвращает из базы список вида:
        [('Abzû2', 1, '2017-07-02'), ('Adrift', 1, '2017-07-02'), ('Agents of Mayhem', 0, None), ...

    :param filter_by_is_cracked: определяет нужно ли фильтровать по полю is_cracked. Если filter_by_is_cracked = None,
    фильтр не используется, иначе фильтрация будет по значению в filter_by_is_cracked

    :param sorted_by_name: использовать ли сортировку по названию игры
    :param sorted_by_crack_date: использовать ли сортировку по crack_date
    :return:
    """

    connect = create_connect()

    sort = ''
    if sorted_by_name:
        sort = ' order by name'

    if sorted_by_crack_date:
        # # Обратный порядок, чтобы первым в списке были самые новые
        # sort = ' order by crack_date desc'

        # NOTE: идея такая: сначала сортировка по дате, а после сортировка по имени
        # среди тех игр, у которых crack_date одинаковый
        sort = ' order by crack_date desc, name asc'

    try:
        if filter_by_is_cracked is None:
            sql = "SELECT name, is_cracked, crack_date FROM Game" + sort
            items = connect.execute(sql).fetchall()

        else:
            sql = "SELECT name, is_cracked, crack_date FROM Game WHERE is_cracked = ?" + sort
            items = connect.execute(sql, (filter_by_is_cracked,)).fetchall()

        return items

    finally:
        connect.close()


if __name__ == '__main__':
    init_db()

    games = get_games()
    print('Games:', len(games), games)

    games = get_games(filter_by_is_cracked=True)
    print('Cracked:', len(games), [name for name, _, _ in games])

    games = get_games(filter_by_is_cracked=False)
    print('Not cracked:', len(games), [name for name, _, _ in games])

    games = get_games(filter_by_is_cracked=True, sorted_by_crack_date=True)
    print('Cracked and sorted:', len(games), [name for name, _, _ in games])
