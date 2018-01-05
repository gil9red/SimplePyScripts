#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_all_games():
    url = 'https://www.bigfishgames.com/download-games/genres/15/hidden-object.html'

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    return [a.text.strip() for a in root.select('#genre_bottom a')]


if __name__ == '__main__':
    games = get_all_games()
    print('Games ({}): {}'.format(len(games), games))
