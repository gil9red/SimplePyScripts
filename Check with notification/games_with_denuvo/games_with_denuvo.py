#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


def get_games_with_denuvo() -> [(str, bool)]:
    """
    Функция со страницы википедии вытаскивает список игр с Denuvo и их статус "Взломан".

    """

    url = 'https://ru.wikipedia.org/wiki/Список_игр,_защищённых_Denuvo'

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    # Таблица "Список защищённых игр"
    table = root.select('.wikitable')[0]

    games = list()

    for tr in table.select('tr'):
        td_list = tr.select('td')

        # Например, текущий tr -- заголовок таблицы и не содержит td
        if not td_list:
            continue

        name = td_list[0].text.strip()
        cracked = td_list[5].text.lower()

        is_cracked = 'да' in cracked or 'yes' in cracked

        # Удаление сносок в названии: "Mad Max[а 1]", "Deus Ex: Mankind Divided[а 3]"
        if '[' in name and ']' in name:
            name = name[:name.index('[')]

        games.append((name, is_cracked))

    return games


def get_games_which_denuvo_is_removed() -> [str]:
    """
    Функция со страницы википедии вытаскивает список игр в которых убрана защита Denuvo.

    """

    url = 'https://ru.wikipedia.org/wiki/Список_игр,_защищённых_Denuvo'

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    # Таблица "Список игр, в которых убрана защита"
    table = root.select('.wikitable')[1]

    games = list()

    for tr in table.select('tr'):
        td_list = tr.select('td')

        # Например, текущий tr -- заголовок таблицы и не содержит td
        if not td_list:
            continue

        name = td_list[0].text.strip()

        # Удаление сносок в названии: "Mad Max[а 1]", "Deus Ex: Mankind Divided[а 3]"
        if '[' in name and ']' in name:
            name = name[:name.index('[')]

        # NOTE: В таблицу добавили пустую <tr><td> из-за чего: 'Добавляю игру с убранной защитой ""'
        if name:
            games.append(name)

    return games


if __name__ == '__main__':
    games_with_denuvo = get_games_with_denuvo()
    print(f'Всего игр с Denuvo {len(games_with_denuvo)}: {games_with_denuvo}\n')

    cracked_games = list(filter(lambda x: x[1], games_with_denuvo))
    print(f'Взломанные ({len(cracked_games)}):')
    for game in sorted(game for game, is_cracked in cracked_games):
        print(game)

    print('\n')

    games_without_denuvo = get_games_which_denuvo_is_removed()
    print(f'Всего игр в которых убрана защита Denuvo ({len(games_without_denuvo)}):')
    for name in games_without_denuvo:
        print(name)
