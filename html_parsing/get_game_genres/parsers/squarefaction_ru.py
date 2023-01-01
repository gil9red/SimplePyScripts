#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup
from base_parser import BaseParser


class SquarefactionRu_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = f'http://squarefaction.ru/main/search/games?q={self.game_name}'
        rs = self.send_get(url)

        root = BeautifulSoup(rs.content, 'html.parser')

        # http://squarefaction.ru/main/search/games?q=dead+space
        if '/main/search/games' in rs.url:
            self.log_info(f'Parsing of game list')

            for game_block in root.select('#games > .entry'):
                title = self.get_norm_text(game_block.select_one('.name'))
                if not self.is_found_game(title):
                    continue

                # <div class="infos">TPS,Survival Horror,Action</div>
                genres = self.get_norm_text(game_block.select_one('.infos')).split(',')

                # Сойдет первый, совпадающий по имени, вариант
                return genres

        # http://squarefaction.ru/game/dead-space
        else:
            self.log_info(f'Parsing of game page')

            game_block = root.select_one('#page-info')
            if game_block:
                title = self.get_norm_text(game_block.select_one('#title'))
                if not self.is_found_game(title):
                    self.log_warn(f'Not match game title {title!r}')

                # <td class="nowraps-links">
                #     <a href="/games?genre=tps">TPS</a>,
                #     <a href="/games?genre=survival-horror">Survival Horror</a>,
                #     <a href="/games?genre=action">Action</a>
                # </td>
                genres = [
                    self.get_norm_text(a) for a in game_block.select('a') if '?genre=' in a['href']
                ]

                # Сойдет первый, совпадающий по имени, вариант
                return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return SquarefactionRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Action RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Action RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: []
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Survival Horror']
