#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from common import get_norm_text
from base_parser import BaseParser


class IwantgamesRu_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        url = f'https://iwantgames.ru/?s={self.game_name}'
        root = self.send_get(url, return_html=True)

        for game_block in root.select('.game__content'):
            title = get_norm_text(game_block.h2.a)
            if not self.is_found_game(title):
                continue

            # <dt>Жанр:</dt>
            # <dd>
            #     <a href="https://iwantgames.ru/rpg/">РПГ</a>,
            #     <a href="https://iwantgames.ru/horror/">Ужасы</a>,
            #     <a href="https://iwantgames.ru/action/">Экшен</a>
            # </dd>
            #   -> ['РПГ', 'Ужасы', 'Экшен']
            dt = game_block.find('dt', text='Жанр:')
            if not dt:
                continue

            dd = dt.find_next_sibling('dd')
            if not dd:
                continue

            genres = [get_norm_text(a) for a in dd.find_all('a')]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return IwantgamesRu_Parser(*args, **kwargs).get_game_genres(game_name)


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
