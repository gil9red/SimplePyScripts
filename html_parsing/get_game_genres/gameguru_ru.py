#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from common import get_norm_text
from base_parser import BaseParser


class GameguruRu_Parser(BaseParser):
    def _parse(self) -> List[str]:
        url = f'https://gameguru.ru/search/all.html?s={self.game_name}'
        root = self.send_get(url, return_html=True)

        for game_block in root.select('.jointCard-result-game-unit'):
            title = get_norm_text(game_block.select_one('.jointCard-result-game-list-title'))
            if not self.is_found_game(title):
                continue

            genres = [get_norm_text(a) for a in game_block.select('a') if '/genre/' in a['href']]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return GameguruRu_Parser(*args, **kwargs).get_game_genres(game_name)


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
