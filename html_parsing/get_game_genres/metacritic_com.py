#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class MetacriticCom_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        url = f'https://www.metacritic.com/search/game/{self.game_name}/results'
        rs = self.send_get(url)
        root = BeautifulSoup(rs.content, 'html.parser')

        for game_block_preview in root.select('.result'):
            a = game_block_preview.select_one('.product_title > a')
            title = get_norm_text(a)
            if not smart_comparing_names(title, self.game_name):
                continue

            url_game = urljoin(rs.url, a['href'])
            self.log_info(f'Load {url_game!r}')

            rs = self.send_get(url_game)

            game_block = BeautifulSoup(rs.content, 'html.parser')
            # <li class="summary_detail product_genre">
            #     <span class="label">Genre(s): </span>
            #     <span class="data">Role-Playing</span>,
            #     <span class="data">Action RPG</span>
            # </li>
            genres = [
                get_norm_text(a) for a in game_block.select('.summary_detail.product_genre > .data')
            ]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return MetacriticCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing', 'First-Person', 'First-Person', 'Western-Style']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Role-Playing', 'Action RPG', 'Action RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Role-Playing', 'Action RPG', 'Action RPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action Adventure', 'Modern', 'General', 'Modern', 'Linear']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Action Adventure', 'Horror', 'Survival']
