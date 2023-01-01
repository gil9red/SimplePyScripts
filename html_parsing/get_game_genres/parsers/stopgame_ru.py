#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from base_parser import BaseParser


class StopgameRu_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = f'https://stopgame.ru/search/?s={self.game_name}&where=games&sort=name'
        root = self.send_get(url, return_html=True)
    
        for game_block in root.select('.game-summary'):
            title = self.get_norm_text(game_block.select_one('.caption'))
            if not self.is_found_game(title):
                continue

            # Сойдет первый, совпадающий по имени, вариант
            return [
                self.get_norm_text(a) for a in game_block.select('a[href*="?genre[]"]')
            ]
    
        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
    return StopgameRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['action', 'rpg']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['rpg']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['action', 'logic']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['action', 'adventure']
