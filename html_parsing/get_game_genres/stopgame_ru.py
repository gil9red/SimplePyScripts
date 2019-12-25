#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class StopgameRu_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        rs = self.send_get(f'https://stopgame.ru/search/?s={self.game_name}&where=games&sort=name')
        root = BeautifulSoup(rs.content, 'html.parser')
    
        for game_block in root.select('.game-block'):
            title = get_norm_text(game_block.select_one('.title'))
            if not smart_comparing_names(title, self.game_name):
                continue
    
            genres = [get_norm_text(a) for a in game_block.select('.game-genre-value > a') if '?genre[]' in a['href']]
    
            # Сойдет первый, совпадающий по имени, вариант
            return genres
    
        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return StopgameRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['action', 'rpg']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['rpg']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['action', 'logic']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['action', 'adventure']
