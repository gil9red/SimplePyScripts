#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class GamerInfoCom_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        form_data = {
            'search-query': self.game_name,
            'search-obl': 'games',
            'page': '1',
        }

        rs = self.send_post('https://gamer-info.com/search-q/', headers=headers, data=form_data)
        root = BeautifulSoup(rs.content, 'html.parser')

        for game_block in root.select('.games > .c2'):
            g = game_block.select_one('.g')
            if 'Жанр:' not in g.text:
                continue

            title = get_norm_text(game_block.select_one('.n'))
            if not smart_comparing_names(title, self.game_name):
                continue

            genres = g.text.replace('Жанр:', '').strip().split(', ')

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return GamerInfoCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['action', 'RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: []
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['action', 'приключения']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['action', 'приключения']
