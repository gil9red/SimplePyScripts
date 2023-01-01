#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from base_parser import BaseParser


class GamespotCom_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = f'https://www.gamespot.com/search/?i=site&q={self.game_name}'
        root = self.send_get(url, return_html=True)

        for game_block_preview in root.select('.media-body'):
            if not game_block_preview.select_one('.media-date'):
                continue

            a = game_block_preview.select_one('.media-title a')
            title = self.get_norm_text(a)
            if not self.is_found_game(title):
                continue

            url_game = urljoin(url, a['href'])
            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)

            tag_object_stats = game_block.select_one('#object-stats-wrap')
            if not tag_object_stats:
                return []

            genres = [self.get_norm_text(a) for a in tag_object_stats.select('a[href]') if '/genre/' in a['href']]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
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
