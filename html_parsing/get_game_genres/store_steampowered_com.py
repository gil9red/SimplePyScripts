#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class StoreSteampoweredCom_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        # category1 = Игры
        url = f'https://store.steampowered.com/search/?term={self.game_name}&category1=998'
        rs = self.send_get(url)
        root = BeautifulSoup(rs.content, 'html.parser')

        for game_block_preview in root.select('.search_result_row'):
            title = get_norm_text(game_block_preview.select_one('.search_name > .title'))
            if not smart_comparing_names(title, self.game_name):
                continue

            href = game_block_preview['href']
            url_game = urljoin(rs.url, href)
            self.log_info(f'Load {url_game!r}')

            rs = self.send_get(url_game)
            game_block = BeautifulSoup(rs.content, 'html.parser')
            # <div class="details_block">
            #     <b>Title:</b> HELLGATE: London<br>
            #     <b>Genre:</b>
            #     <a href="https://store.steampowered.com/genre/Action/?snr=1_5_9__408">Action</a>,
            #     <a href="https://store.steampowered.com/genre/RPG/?snr=1_5_9__408">RPG</a>
            genres = [
                get_norm_text(a) for a in game_block.select('.details_block > a[href*="/genre/"]')
            ]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
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
