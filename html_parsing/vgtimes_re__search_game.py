#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup, Tag


URL_BASE = 'https://vgtimes.ru/'


@dataclass
class Game:
    title: str
    date: str
    genres: list[str] = field(default_factory=list)

    @classmethod
    def parse(cls, game_el: Tag) -> 'Game':
        return cls(
            title=game_el.select_one('.title').text.strip(),
            date=game_el.select_one('.date').text.strip(),
            genres=game_el.select_one('.genre').text.strip().split(', '),
        )


session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'


def search(game_name: str) -> list[Game]:
    rs = session.get(URL_BASE)
    rs.raise_for_status()

    url_search = f'{URL_BASE}engine/ajax/search.php'
    data = {
        'action': 'search2',
        'query': game_name,
        'ismobile': '',
        'what': 1,
    }

    rs = session.post(url_search, data=data)
    rs.raise_for_status()

    rs_html = rs.json()['games_result']
    root = BeautifulSoup(rs_html, 'html.parser')

    return [
        Game.parse(game_el)
        for game_el in root.select('.game_search')
    ]


if __name__ == '__main__':
    games = search('Dead Space')
    print(f'Games ({len(games)}):')
    for i, game in enumerate(games, 1):
        print(f'    {i}. {game}')
    """
    Games (9):
        1. Game(title='Dead Space', date='27 января 2023', genres=['Экшен', 'Шутер', 'Вид от третьего лица', 'Футуризм (Будущее)', 'Хоррор на выживание'])
        2. Game(title='Dead Space 2', date='25 января 2011', genres=['Экшен', 'Шутер', 'Хоррор', 'Вид от третьего лица', 'Футуризм (Будущее)'])
        3. Game(title='Dead Space 3', date='5 февраля 2013', genres=['Экшен', 'Вид от третьего лица'])
        4. Game(title='Dead Space (2008)', date='14 октября 2008', genres=['Экшен', 'Приключение', 'Хоррор', 'Вид от третьего лица', 'Футуризм (Будущее)'])
        5. Game(title='Dead Space: Extraction', date='25 сентября 2009', genres=['Экшен', 'Шутер', 'Хоррор', 'Вид от первого лица', 'Футуризм (Будущее)', 'Кооператив (co-op)'])
        6. Game(title='Dead Space Ignition', date='13 октября 2010', genres=['Аркада', 'Логическая'])
        7. Game(title="Alekhine's Gun", date='1 марта 2016', genres=['Экшен', 'Приключение', 'Стелс', 'Вид от третьего лица'])
        8. Game(title='Смерть шпионам', date='1 марта 2007', genres=['Экшен', 'Шутер', 'Стелс', 'Вид от первого лица', 'Вид от третьего лица'])
        9. Game(title='Смерть шпионам: Момент истины', date='28 марта 2008', genres=['Экшен', 'Шутер', 'Стелс', 'Вид от первого лица', 'Вид от третьего лица'])
    """