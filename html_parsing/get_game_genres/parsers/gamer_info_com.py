#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from base_parser import BaseParser


class GamerInfoCom_Parser(BaseParser):
    def _parse(self) -> list[str]:
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        form_data = {
            'search-query': self.game_name,
            'search-obl': 'games',
            'page': '1',
        }

        url = 'https://gamer-info.com/search-q/'
        root = self.send_post(url, headers=headers, data=form_data, return_html=True)

        for game_block in root.select('.games > .c2'):
            g = game_block.select_one('.g')
            if 'Жанр:' not in g.text:
                continue

            title = self.get_norm_text(game_block.select_one('.n'))
            if not self.is_found_game(title):
                continue

            genres = g.text.replace('Жанр:', '').strip().split(', ')

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return GamerInfoCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['action', 'RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: []
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['action', 'приключения']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['action', 'приключения']
