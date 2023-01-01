#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from base_parser import BaseParser


class MobygamesCom_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = f'https://www.mobygames.com/search/quick?q={self.game_name}&p=3&search=Go&sFilter=1&sG=on'
        root = self.send_get(url, return_html=True)

        for game_block_preview in root.select('.searchTitle > a'):
            title = self.get_norm_text(game_block_preview)
            if not self.is_found_game(title):
                continue

            href = game_block_preview['href']
            url_game = urljoin(url, href)

            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)
            genres = game_block\
                .select_one('#coreGameGenre').find_next('div', text='Genre')\
                .find_next_sibling('div').find_all('a')

            genres = [self.get_norm_text(a) for a in genres]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return MobygamesCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing (RPG)']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Action', 'Role-Playing (RPG)']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Action', 'Role-Playing (RPG)']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Action']
