#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class GameGuruRu_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        rs = self.send_get(f'https://gameguru.ru/search/all.html?s={self.game_name}')
        root = BeautifulSoup(rs.content, 'html.parser')

        for game_block in root.select('.jointCard-result-game-unit'):
            title = get_norm_text(game_block.select_one('.jointCard-result-game-list-title'))
            if not smart_comparing_names(title, self.game_name):
                continue

            genres = [get_norm_text(a) for a in game_block.select('a') if '/genre/' in a['href']]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return GameGuruRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Экшен', 'RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['RPG', 'aRPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Экшен']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Экшен', 'Шутер', 'Квест']
