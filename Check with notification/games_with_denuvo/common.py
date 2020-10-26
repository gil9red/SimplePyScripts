#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')


from all_common import get_logger, wait, simple_send_sms


# make_backslashreplace_console()


DEBUG = False
# DEBUG = True


if DEBUG:
    DB_FILE_NAME = 'test.database.sqlite'

    log = get_logger('test_games_with_denuvo', file='test_log.txt')
    log_cracked_games = get_logger('test_cracked_games', file='test_cracked_games.log.txt', log_stdout=False)

else:
    DB_FILE_NAME = 'database.sqlite'

    log = get_logger('games_with_denuvo')
    log_cracked_games = get_logger('cracked_games', file='cracked_games.log.txt', log_stdout=False)


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
                
                append_date TIMESTAMP DEFAULT NULL,
                release_date TIMESTAMP DEFAULT NULL,
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
        #
        #         append_date TIMESTAMP DEFAULT NULL,
        #         release_date TIMESTAMP DEFAULT NULL,
        #         crack_date TIMESTAMP DEFAULT NULL,
        #
        #         CONSTRAINT name_unique UNIQUE (name)
        #     );
        #
        #     -- INSERT INTO Game2 SELECT id, name, is_cracked, date('now'), crack_date FROM Game;
        #     INSERT INTO Game2 (id, name, is_cracked, append_date, crack_date)
        #         SELECT id, name, is_cracked, append_date, crack_date FROM Game;
        #
        #     DROP TABLE Game;
        #     ALTER TABLE Game2 RENAME TO Game;
        # ''')

        connect.commit()

    finally:
        connect.close()


def db_create_backup(backup_dir='backup'):
    from datetime import datetime
    file_name = str(datetime.today().date()) + '.sqlite'

    import os
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    file_name = os.path.join(backup_dir, file_name)

    import shutil
    shutil.copy(DB_FILE_NAME, file_name)


def update_release_date(connect, name: str, release_date: DT.date):
    sql = "UPDATE Game SET release_date = ? WHERE name = ? AND release_date IS NULL"
    connect.execute(sql, [release_date, name])


def append_list_games(games: [(str, DT.date, bool)], notified_by_sms=True):
    connect = create_connect()

    def insert(name: str, release_date: DT.date, is_cracked: bool) -> bool:
        # Для отсеивания дубликатов
        has = connect.execute("SELECT 1 FROM Game WHERE name = ?", [name]).fetchone()
        if has:
            return False

        log.debug(f'Добавляю {name!r} ({is_cracked})')
        sql = "INSERT OR IGNORE INTO Game (name, is_cracked, append_date, release_date) VALUES (?, ?, date('now'), ?)"
        connect.execute(sql, [name, is_cracked, release_date])

        # Если добавлена уже взломанная игра, указываем дату
        if is_cracked:
            connect.execute("UPDATE Game SET crack_date = date('now') WHERE name = ?", [name])

        return True

    try:
        for name, release_date, is_cracked in games:
            ok = insert(name, release_date, is_cracked)

            update_release_date(connect, name, release_date)

            # Игра уже есть в базе, нужно проверить ее статус is_cracked, возможно, он поменялся и игру взломали
            if not ok:
                rs_is_cracked = connect.execute('SELECT is_cracked FROM Game where name = ?', [name]).fetchone()[0]

                # Если игра раньше имела статус is_cracked = False, а теперь он поменялся на True:
                if not rs_is_cracked and is_cracked:
                    # Поменяем флаг у игры в базе
                    connect.execute("UPDATE Game SET is_cracked = 1, crack_date = date('now') WHERE name = ?", [name])

                    text = f'Игру {name!r} взломали'
                    log.info(text)
                    log_cracked_games.debug(text)

                    # При DEBUG = True, отправки смс не будет
                    if notified_by_sms and not DEBUG:
                        simple_send_sms(text, log)

            elif is_cracked:
                text = f'Добавлена взломанная игра {name!r}'
                log.info(text)
                log_cracked_games.debug(text)

                # При DEBUG = True, отправки смс не будет
                if notified_by_sms and not DEBUG:
                    simple_send_sms(text, log)

        connect.commit()

    finally:
        connect.close()


def append_list_games_which_denuvo_is_removed(games: [str, DT.date], notified_by_sms=True):
    connect = create_connect()

    def insert(name: str, release_date: DT.date) -> bool:
        # Для отсеивания дубликатов
        has = connect.execute("SELECT 1 FROM Game WHERE name = ?", [name]).fetchone()
        if has:
            return False

        log.debug(f'Добавляю игру с убранной защитой {name!r}')

        sql = "INSERT OR IGNORE INTO Game (name, is_cracked, append_date, crack_date, release_date) " \
              "VALUES (?, 1, date('now'), date('now'), ?)"
        connect.execute(sql, [name, release_date])
        return True

    try:
        for name, release_date in games:
            ok = insert(name, release_date)

            update_release_date(connect, name, release_date)

            # Игра уже есть в базе, нужно проверить ее статус is_cracked, возможно, он поменялся и игру взломали
            if ok:
                text = f'Добавлена игра с убранной защитой {name!r}'
                log.info(text)
                log_cracked_games.debug(text)

                # При DEBUG = True, отправки смс не будет
                if notified_by_sms and not DEBUG:
                    simple_send_sms(text, log)

            else:
                rs_is_cracked = connect.execute('SELECT is_cracked FROM Game where name = ?', [name]).fetchone()[0]

                # Если игра раньше имела статус is_cracked = False
                if not rs_is_cracked:
                    # Поменяем флаг у игры в базе
                    connect.execute("UPDATE Game SET is_cracked = 1, crack_date = date('now') WHERE name = ?", [name])

                    text = f'Игре {name!r} убрали защиту'
                    log.info(text)
                    log_cracked_games.debug(text)

                    # При DEBUG = True, отправки смс не будет
                    if notified_by_sms and not DEBUG:
                        simple_send_sms(text, log)

        connect.commit()

    finally:
        connect.close()


def get_games(filter_by_is_cracked=None, sorted_by_name=True,
              sorted_by_crack_date=False, sorted_by_append_date=False) -> [(str, bool, str, str, str)]:
    """
    Функция возвращает из базы список вида:
        [('Monopoly Plus', 1, '12/09/2017', '07/10/2017 '), ('FIFA 18', 1, '18/09/2017', '03/10/2017 '), ...

    :param filter_by_is_cracked: определяет нужно ли фильтровать по полю is_cracked. Если filter_by_is_cracked = None,
    фильтр не используется, иначе фильтрация будет по значению в filter_by_is_cracked

    :param sorted_by_name: использовать ли сортировку по названию игры
    :param sorted_by_crack_date: использовать ли сортировку по crack_date
    :param sorted_by_append_date: использовать ли сортировку по append_date
    :return:
    """

    log.debug('Start get_games: filter_by_is_cracked=%s, sorted_by_name=%s, sorted_by_crack_date=%s',
              filter_by_is_cracked, sorted_by_name, sorted_by_crack_date)

    connect = create_connect()

    sort = ''
    if sorted_by_name:
        sort = ' ORDER BY name'

    if sorted_by_crack_date:
        # NOTE: идея такая: сначала сортировка по дате, а после сортировка по имени
        # среди тех игр, у которых crack_date одинаковый
        sort = ' ORDER BY crack_date DESC, name ASC'

    if sorted_by_append_date:
        sort = ' ORDER BY append_date DESC, name ASC'

    try:
        sql = """
        SELECT name, is_cracked, 
            strftime('%d/%m/%Y', append_date), 
            strftime('%d/%m/%Y', crack_date), 
            strftime('%d/%m/%Y', release_date) 
        FROM Game
        """

        if filter_by_is_cracked is not None:
            sql += ' WHERE is_cracked = ' + str(int(filter_by_is_cracked))

        sql += sort

        log.debug('sql: %s', sql)
        items = connect.execute(sql).fetchall()

        log.debug('Finish get_games: items[%s]: %s', len(items), items)

        return items

    finally:
        connect.close()


if __name__ == '__main__':
    init_db()

    games = get_games()
    print('Games:', len(games), games)
    print('\n' + '-' * 100 + '\n')

    games = get_games(filter_by_is_cracked=True)
    print('Cracked:', len(games), [name for name, _, _, _, _ in games])
    print('\n' + '-' * 100 + '\n')

    games = get_games(filter_by_is_cracked=False)
    print('Not cracked:', len(games), [name for name, _, _, _, _ in games])
    print('\n' + '-' * 100 + '\n')

    games = get_games(filter_by_is_cracked=True, sorted_by_crack_date=True)
    print('Cracked and sorted:', len(games), [name for name, _, _, _, _ in games])
    print('\n' + '-' * 100 + '\n')

    games = get_games(filter_by_is_cracked=False, sorted_by_append_date=True)
    print('Not cracked and sorted by append:', len(games), [name for name, _, _, _, _ in games])
