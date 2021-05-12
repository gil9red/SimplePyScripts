#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List

from base_parser import BaseParser


class PlaygroundRu_Parser(BaseParser):
    def _parse(self) -> List[str]:
        url = f'https://www.playground.ru/search/?q={self.game_name}&filter=game'
        root = self.send_get(url, return_html=True)

        for game_block_preview in root.select('.search-results .title'):
            title = self.get_norm_text(game_block_preview)
            if not self.is_found_game(title):
                continue

            url_game = urljoin(url, game_block_preview['href'])
            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)
            # <div class="genres">
            #     <a class="item" href="/games/action/">Экшен</a>
            #     <meta itemprop="genre" content="Экшен">
            #     <a class="item" href="/games/rpg/">Ролевая</a>
            #     <meta itemprop="genre" content="Ролевая">
            genres = [
                self.get_norm_text(a) for a in game_block.select('.genres > .item')
            ]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return PlaygroundRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Экшен', 'Ролевая', 'От первого лица', 'От третьего лица', 'Фэнтези']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Экшен', 'Ролевая', 'Стимпанк']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['Экшен']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Экшен', 'Адвенчура', 'Ужасы', 'От первого лица']
