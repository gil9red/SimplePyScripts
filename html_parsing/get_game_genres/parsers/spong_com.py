#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from base_parser import BaseParser


class SpongCom_Parser(BaseParser):
    def _parse(self) -> list[str]:
        url = f'https://spong.com/search/index.jsp?q={self.game_name}'
        root = self.send_get(url, return_html=True)
    
        # Первая таблица -- та, что нужна нам
        result = root.select_one('table.searchResult')
        if result:
            for game_block in result.select('tr'):
                tds = game_block.select('td')
                if len(tds) != 4:  # Например, tr > th
                    continue

                td_title, _, genres_td, platforms_td = tds

                title = self.get_norm_text(td_title.a)
                if not self.is_found_game(title):
                    continue

                # <td>Adventure: Free Roaming<br/>Adventure: Survival Horror<br/></td>
                #   -> ['Adventure: Free Roaming', 'Adventure: Survival Horror']
                genres = list(genres_td.stripped_strings)

                # Сойдет первый, совпадающий по имени, вариант
                return genres
    
        self.log_info(f'Not found game {self.game_name!r}')
        return []


def get_game_genres(game_name: str, *args, **kwargs) -> list[str]:
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
