#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых игр серии Spirits of Mystery.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')


from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait


make_backslashreplace_console()


log = get_logger('new game Spirits of Mystery')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/19da316dae6d07d26e6cfc29f401d6142a70ad2c/bigfishgames.com__hidden-object/get_all_games.py
# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/19da316dae6d07d26e6cfc29f401d6142a70ad2c/bigfishgames.com__hidden-object/find__Spirits%20of%20Mystery__of__Collector's%20Edition.py
def get_all_games__spirits_of_mystery():
    url = 'https://www.bigfishgames.com/download-games/genres/15/hidden-object.html'

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    prefix = "Spirits of Mystery".upper()
    postfix = "Collector's Edition".upper()

    games = [a.text.strip() for a in root.select('#genre_bottom a')]
    return [game for game in games if game.upper().startswith(prefix) and game.upper().endswith(postfix)]


FILE_NAME_CURRENT_GAMES = 'games'


def save_items(items):
    open(FILE_NAME_CURRENT_GAMES, mode='w', encoding='utf-8').write(str(items))


if __name__ == '__main__':
    notified_by_sms = True

    # Загрузка текущих игр
    try:
        import ast
        current_games = ast.literal_eval(open(FILE_NAME_CURRENT_GAMES, encoding='utf-8').read())

    except:
        current_games = []

    log.debug('Current games(%s): %s', len(current_games), current_games)

    while True:
        try:
            log.debug('get games')

            games = get_all_games__spirits_of_mystery()
            log.debug('games: %s', games)

            # Если список текущих игр
            if not current_games:
                log.debug('Обнаружен первый запуск')

                current_games = games
                save_items(current_games)

            else:
                new_games = set(games) - set(current_games)
                if new_games:
                    current_games = games
                    save_items(current_games)

                    for game in new_games:
                        text = 'Появилась новая игра "{}"'.format(game)
                        log.debug(text)

                        if notified_by_sms:
                            simple_send_sms(text, log)

                else:
                    log.debug('Новых игр нет')

            wait(weeks=1)

        except:
            log.exception('Ошибка:')
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
