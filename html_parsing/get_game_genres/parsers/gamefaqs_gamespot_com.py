#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from base_parser import BaseParser


class GamefaqsGamespotCom_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = f'https://gamefaqs.gamespot.com/search?game={self.game_name}'
        root = self.send_get(url, return_html=True)

        for game_block_preview in root.select('.search_results_title > .search_result'):
            a = game_block_preview.select_one('.sr_name > a.log_search')
            title = self.get_norm_text(a)
            if not self.is_found_game(title):
                continue

            url_game = urljoin(url, a['href'])
            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)
            game_info = game_block.select_one('.pod_gameinfo_left')
            if not game_info:
                return []

            # <li><b>Genre:</b>
            # <a href="/pc/category/54-action">Action</a> »
            # <a href="/pc/category/55-action-shooter">Shooter</a> »
            # <a href="/pc/category/80-action-shooter-third-person">Third-Person</a> »
            # <a href="/pc/category/182-action-shooter-third-person-arcade">Arcade</a>
            # </li>
            genres = [
                self.get_norm_text(a)
                for a in game_info.select_one('li > b:contains("Genre:")').find_next_siblings('a')
            ]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return GamefaqsGamespotCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing', 'Western-Style']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Role-Playing', 'Action RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Role-Playing', 'Action RPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action Adventure', 'Linear']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Action Adventure', 'Survival']
