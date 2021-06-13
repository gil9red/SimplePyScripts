#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

import requests
from bs4 import BeautifulSoup


DEFAULT_URL = 'https://www.bigfishgames.com/download-games/genres/15/hidden-object.html'


def get_all_games(url=DEFAULT_URL, prefix='', postfix='') -> List[str]:
    def is_valid(game: str) -> bool:
        game = game.upper()
        return game.startswith(prefix.upper()) and game.endswith(postfix.upper())

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    return [a.text.strip() for a in root.select('#genre_bottom a') if is_valid(a.text.strip())]


if __name__ == '__main__':
    games = get_all_games()
    print(f'Games ({len(games)}): {games}')

    import json
    json.dump(games, open('games.json', 'w', encoding='utf-8'), ensure_ascii=False)
