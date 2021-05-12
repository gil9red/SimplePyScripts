#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from typing import List

from base_parser import BaseParser


class AgRu_Parser(BaseParser):
    def _parse(self) -> List[str]:
        headers = {
            'Host': 'ag.ru',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }

        # Для правдоподобности сделаем запрос на страницу с играми
        rs = self.send_get('https://ag.ru/games/pc', headers=headers)
        m = re.search(r'"rawgApiKey"\s*:\s*"(.+?)"', rs.text)
        if not m:
            raise Exception('Не удалось найти на странице ключ для API (rawgApiKey)!')
        key = m.group(1)

        # Заголовки, что отправляются вместе с запросом к API
        headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Referer': 'https://ag.ru/games/pc',
            'X-API-Language': 'ru',
            'X-API-Referer': '%2Fgames',
            'X-API-Client': 'website',
        })

        url = f'https://ag.ru/api/games?page_size=20&search={self.game_name}&page=1&key={key}'
        rs = self.send_get(url, headers=headers)

        for item in rs.json()['results']:
            title = item['name']
            if not self.is_found_game(title):
                continue

            genres = [x['name'] for x in item['genres']]

            # Сойдет первый, совпадающий по имени, вариант
            return genres

        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return AgRu_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Шутеры', 'Экшены', 'Ролевые']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: []
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Экшены', 'Ролевые']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Приключения', 'Экшены']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Шутеры']
