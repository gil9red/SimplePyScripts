#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from base_parser import BaseParser


class IwgsGames_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = 'https://iwgs.games/'

        root = self.send_post(url, data=dict(s=self.game_name), return_html=True)
        for a in root.select('.games h2 > a'):
            title = self.get_norm_text(a)
            if not self.is_found_game(title):
                continue

            url_game = urljoin(url, a['href'])
            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)

            genres_el = game_block.select('.genre > a')
            genres = [self.get_norm_text(a) for a in genres_el]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return IwgsGames_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test, TEST_GAMES
    TEST_GAMES.append('Dark Souls: Remastered')

    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: []
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: []
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: []
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: []
    #
    # Search 'Dark Souls: Remastered'...
    #     Genres: ['РПГ', 'Ужасы', 'Экшен']
