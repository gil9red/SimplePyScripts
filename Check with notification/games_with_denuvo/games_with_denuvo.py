#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

import requests
from bs4 import BeautifulSoup


def get_games_with_denuvo() -> [(str, DT.date, bool)]:
    """
    Функция со страницы википедии вытаскивает список игр с Denuvo, с датой выхода и статусом "Взломан".

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

        name = td_list[0].get_text(strip=True)

        # Удаление сносок в названии: "Mad Max[а 1]", "Deus Ex: Mankind Divided[а 3]"
        if '[' in name and ']' in name:
            name = name[:name.index('[')]

        # Example: '23.09.2014'
        try:
            date_str = td_list[3].get_text(strip=True)
            date = DT.datetime.strptime(date_str, '%d.%m.%Y').date()
        except:
            date = None

        cracked = td_list[5].text.lower()
        is_cracked = 'да' in cracked or 'yes' in cracked

        games.append((name, date, is_cracked))

    return games


def get_games_which_denuvo_is_removed() -> [str, DT.date]:
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

        # Example: '23.09.2014'
        try:
            date_str = td_list[3].get_text(strip=True)
            date = DT.datetime.strptime(date_str, '%d.%m.%Y').date()
        except:
            date = None

        # NOTE: В таблицу добавили пустую <tr><td> из-за чего: 'Добавляю игру с убранной защитой ""'
        if name:
            games.append((name, date))

    return games


if __name__ == '__main__':
    games_with_denuvo = get_games_with_denuvo()
    print(f'Всего игр с Denuvo {len(games_with_denuvo)}: {games_with_denuvo}\n')

    cracked_games = list(filter(lambda x: x[-1], games_with_denuvo))
    print(f'Взломанные ({len(cracked_games)}):')
    for game in sorted(game for game, date, is_cracked in cracked_games):
        print(game)

    print('\n')

    games_without_denuvo = get_games_which_denuvo_is_removed()
    print(f'Всего игр в которых убрана защита Denuvo ({len(games_without_denuvo)}):')
    for name, _ in games_without_denuvo:
        print(name)
