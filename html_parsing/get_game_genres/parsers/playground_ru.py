#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from base_parser import BaseParser


class PlaygroundRu_Parser(BaseParser):
    base_url = 'https://www.playground.ru'

    def _parse(self) -> list[str]:
        url = f'{self.base_url}/api/game.search?query={self.game_name}&include_addons=1'
        data = self.send_get(url).json()

        for game in data:
            title = game['name']
            if not self.is_found_game(title):
                continue

            url_game = urljoin(self.base_url, game['slug'])
            self.log_info(f'Load {url_game!r}')

            game_block = self.send_get(url_game, return_html=True)
            genres = [
                self.get_norm_text(x).strip(',') for x in game_block.select('.genres > a')
            ]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
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
