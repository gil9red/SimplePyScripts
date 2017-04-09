#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_games_with_denuvo() -> [(str, bool)]:
    """
    Функция со страницы википедии вытаскивает список игр с Denuvo и их статус "Взломан".

    """

    # Так-то скрипт работает и ru, с en
    url = 'https://en.wikipedia.org/wiki/Denuvo'
    # url = 'https://ru.wikipedia.org/wiki/Denuvo'

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    # Таблица "Список защищённых игр"
    table = root.select('.wikitable')[0]

    games = list()

    for tr in table.select('tr'):
        td_list = tr.select('td')

        # Например, текущий tr -- заголовок таблицы и не содержит td
        if not td_list:
            continue

        name = td_list[0].text.strip()
        cracked = td_list[-1].text.lower()

        is_cracked = 'да' in cracked or 'yes' in cracked

        # Удаление сносок в названии: "Mad Max[а 1]", "Deus Ex: Mankind Divided[а 3]"
        if '[' in name and ']' in name:
            name = name[:name.index('[')]

        games.append((name, is_cracked))

    return games


if __name__ == '__main__':
    games_with_denuvo = get_games_with_denuvo()

    print('Всего игр с Denuvo {}: {}'.format(len(games_with_denuvo), games_with_denuvo))
    cracked_games = list(filter(lambda x: x[1], games_with_denuvo))

    print()
    print('Взломанные ({}):'.format(len(cracked_games)))
    for game in sorted(game for game, is_cracked in cracked_games):
        print(game)
