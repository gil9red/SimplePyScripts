#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class GamespotCom_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        url = f'https://www.gamespot.com/search/?i=site&q={self.game_name}'
        rs = self.send_get(url)
        root = BeautifulSoup(rs.content, 'html.parser')

        for game_block_preview in root.select('.media-body'):
            if not game_block_preview.select_one('.media-date'):
                continue

            a = game_block_preview.select_one('.media-title a')
            title = get_norm_text(a)

            if not smart_comparing_names(title, self.game_name):
                continue

            url_game = urljoin(rs.url, a['href'])
            self.log_info(f'Load {url_game!r}')

            rs = self.send_get(url_game)
            if not rs.ok:
                self.log_warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
                continue

            game_block = BeautifulSoup(rs.content, 'html.parser')
            tag_object_stats = game_block.select_one('#object-stats-wrap')
            if not tag_object_stats:
                return []

            genres = [get_norm_text(a) for a in tag_object_stats.select('a[href]') if '/genre/' in a['href']]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return GamespotCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Role-Playing', 'Action']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action', 'Adventure']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Adventure', 'Survival', '3D', 'Action']
