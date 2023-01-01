#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from base_parser import BaseParser


class GameguruRu_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url_search = f'https://gameguru.ru/games/?search={self.game_name}'

        page = last_page = 1
        while page <= last_page:
            url = url_search
            if page > 1:
                url = f'{url_search}&page={page}'

            self.log_info(f'Load {url!r}')
            root = self.send_get(url, return_html=True)

            for game_block in root.select('#publications-wrap .short-news-content'):
                title = self.get_norm_text(game_block.select_one('.short-news-title'))
                if not self.is_found_game(title):
                    continue

                for info in game_block.select('.short-news-play-info'):
                    if 'Жанр'.upper() not in self.get_norm_text(info).upper():
                        continue

                    return [self.get_norm_text(x) for x in info.select('div > span')]

            # Обновление номера последней страницы
            pages = root.select('.pagination a.page-link[href]')
            if pages:
                href = pages[-1]['href']
                m = re.search(r'&page=(\d+)', href)
                last_page = int(m.group(1))

            page += 1

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return GameguruRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Экшен', 'RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['RPG', 'aRPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Экшен']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Экшен', 'Шутер', 'Квест']
