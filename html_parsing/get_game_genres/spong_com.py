#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from bs4 import BeautifulSoup

from common import smart_comparing_names, get_norm_text
from base_parser import BaseParser


class SpongCom_Parser(BaseParser):
    def get_site_name(self):
        import os.path
        return os.path.splitext(os.path.basename(__file__))[0]

    def _parse(self) -> List[str]:
        url = f'https://spong.com/search/index.jsp?q={self.game_name}'
        rs = self.send_get(url)
        root = BeautifulSoup(rs.content, 'html.parser')
    
        # Первая таблица -- та, что нужна нам
        for game_block in root.select_one('table.searchResult').select('tr'):
            tds = game_block.select('td')
            if len(tds) != 4:  # Например, tr > th
                continue
    
            td_title, _, genres_td, platforms_td = tds
    
            title = get_norm_text(td_title.a)
            if not smart_comparing_names(title, self.game_name):
                continue

            # <td>Adventure: Free Roaming<br/>Adventure: Survival Horror<br/></td>
            #   -> ['Adventure: Free Roaming', 'Adventure: Survival Horror']
            genres = list(genres_td.stripped_strings)
    
            # Сойдет первый, совпадающий по имени, вариант
            return genres
    
        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> List[str]:
    return SpongCom_Parser(*args, **kwargs).get_game_genres(game_name)


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Adventure: Survival Horror']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Adventure: Role Playing']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Adventure: Role Playing']
    #
    # Search 'Twin Sector'...
    #     Genres: []
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Adventure: Survival Horror']
