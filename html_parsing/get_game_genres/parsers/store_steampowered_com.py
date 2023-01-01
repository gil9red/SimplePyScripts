#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from base_parser import BaseParser


class StoreSteampoweredCom_Parser(BaseParser):
    def _parse(self) -> list[str]:
        # category1 = Игры
        url = 'https://store.steampowered.com/search/'
        params = dict(
            term=self.game_name,
            ndl=1,
            category1=998
        )
        root = self.send_get(url, params=params, return_html=True)

        for game_block_preview in root.select('.search_result_row'):
            title = self.get_norm_text(game_block_preview.select_one('.search_name > .title'))
            if not self.is_found_game(title):
                continue

            href = game_block_preview['href']
            url_game = urljoin(url, href)
            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)
            genres = [
                self.get_norm_text(a) for a in game_block.select('.details_block a[href*="/genre/"]')
            ]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return StoreSteampoweredCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Action', 'RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Action', 'Adventure', 'Indie', 'RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Action', 'RPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action', 'Adventure']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: []
