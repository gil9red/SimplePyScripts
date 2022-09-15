#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from dataclasses import dataclass, field
from typing import Any

import requests

from seconds_to_str import seconds_to_str


@dataclass
class Game:
    id: int
    title: str
    aliases: list[str]

    duration_main_seconds: int  # Main Story
    duration_main_title: str = field(init=False)

    duration_plus_seconds: int  # Main + Sides
    duration_plus_title: str = field(init=False)

    duration_100_seconds: int  # Completionist
    duration_100_title: str = field(init=False)

    duration_all_seconds: int  # All Styles
    duration_all_title: str = field(init=False)

    release_world: int
    profile_platforms: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.duration_main_title = seconds_to_str(self.duration_main_seconds)
        self.duration_plus_title = seconds_to_str(self.duration_plus_seconds)
        self.duration_100_title = seconds_to_str(self.duration_100_seconds)
        self.duration_all_title = seconds_to_str(self.duration_all_seconds)

    @classmethod
    def parse(cls, data: dict[str, Any]) -> 'Game':
        return cls(
            id=data['game_id'],
            title=data['game_name'],
            aliases=data['game_alias'].split(', '),
            duration_main_seconds=data['comp_main'],
            duration_plus_seconds=data['comp_plus'],
            duration_100_seconds=data['comp_100'],
            duration_all_seconds=data['comp_all'],
            release_world=data['release_world'],
            profile_platforms=data['profile_platform'].split(', '),
        )


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'

URL_BASE = 'https://howlongtobeat.com'
URL_SEARCH = f'{URL_BASE}/api/search'


session = requests.session()
session.headers['User-Agent'] = USER_AGENT


def api_search(text: str, page: int = 1) -> dict[str, Any]:
    headers = {
        'Referer': f'{URL_BASE}/?q={text}',
    }
    data = {
        "searchType": "games",
        "searchTerms": text.split(),
        "searchPage": page,
        "size": 20,
        "searchOptions": {
            "games": {
                "userId": 0,
                "platform": "",
                "sortCategory": "popular",
                "rangeCategory": "main",
                "rangeTime": {
                    "min": 0,
                    "max": 0
                },
                "gameplay": {
                    "perspective": "",
                    "flow": "",
                    "genre": ""
                },
                "modifier": ""
            },
            "users": {
                "sortCategory": "postcount"
            },
            "filter": "",
            "sort": 0,
            "randomizer": 0
        }
    }

    rs = session.post(URL_SEARCH, headers=headers, json=data)
    rs.raise_for_status()

    return rs.json()


# TODO: def search(text: str) -> list[Game]:


if __name__ == '__main__':
    text = 'Final Fantasy IX'
    result = api_search(text)
    print(result)
    # {'color': 'blue', 'title': '', 'category': 'games', 'count': 7, 'pageCurrent': 1, 'pageTotal': 1, 'pageSize': 20, 'data': [{'count': 7, 'game_id': 3505, 'game_name': 'Final Fantasy IX', 'game_name_date': 0, 'game_alias': 'Final Fantasy 9, FF9', 'game_type': 'game', 'game_image': 'Ffixbox.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_lvl_spd': 1, 'comp_main': 139631, 'comp_plus': 191277, 'comp_100': 293791, 'comp_all': 172652, 'comp_main_count': 652, 'comp_plus_count': 652, 'comp_100_count': 154, 'comp_all_count': 1458, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 3299, 'count_speedrun': 7, 'count_backlog': 5107, 'count_review': 1173, 'review_score': 89, 'count_playing': 62, 'count_retired': 219, 'profile_dev': 'Square', 'profile_popular': 419, 'profile_steam': 377840, 'profile_platform': 'Mobile, Nintendo Switch, PC, PlayStation, PlayStation 4, Xbox One', 'release_world': 2000}, {'count': 7, 'game_id': 3519, 'game_name': 'Final Fantasy VI', 'game_name_date': 0, 'game_alias': 'Final Fantasy III [NA], Final Fantasy 3 [NA], Final Fantasy 6, FF6, Final Fantasy VI Advance, Final Fantasy VI: Pixel Remaster', 'game_type': 'game', 'game_image': '3519_Final_Fantasy_VI.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_lvl_spd': 1, 'comp_main': 126318, 'comp_plus': 149218, 'comp_100': 230319, 'comp_all': 150133, 'comp_main_count': 251, 'comp_plus_count': 482, 'comp_100_count': 113, 'comp_all_count': 846, 'invested_co': 201600, 'invested_mp': 0, 'invested_co_count': 1, 'invested_mp_count': 0, 'count_comp': 1919, 'count_speedrun': 3, 'count_backlog': 3644, 'count_review': 747, 'review_score': 88, 'count_playing': 43, 'count_retired': 174, 'profile_dev': 'Square', 'profile_popular': 293, 'profile_steam': 1173820, 'profile_platform': 'Game Boy Advance, Mobile, PC, PlayStation, Super Nintendo', 'release_world': 1994}, {'count': 7, 'game_id': 3480, 'game_name': 'Final Fantasy', 'game_name_date': 0, 'game_alias': 'Final Fantasy 1, FF1, Final Fantasy: Pixel Remaster', 'game_type': 'game', 'game_image': '250px-FF1_USA_boxart.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_lvl_spd': 1, 'comp_main': 60291, 'comp_plus': 78627, 'comp_100': 82176, 'comp_all': 69631, 'comp_main_count': 547, 'comp_plus_count': 422, 'comp_100_count': 255, 'comp_all_count': 1224, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 2220, 'count_speedrun': 5, 'count_backlog': 1310, 'count_review': 845, 'review_score': 71, 'count_playing': 47, 'count_retired': 122, 'profile_dev': 'Square', 'profile_popular': 215, 'profile_steam': 1173770, 'profile_platform': 'Browser, Game Boy Advance, Mobile, NES, Nintendo 3DS, PC, PlayStation, PlayStation Portable, WonderSwan', 'release_world': 1987}, {'count': 7, 'game_id': 3516, 'game_name': 'Final Fantasy V', 'game_name_date': 0, 'game_alias': 'Final Fantasy 5, FF5, Final Fantasy V: Pixel Remaster', 'game_type': 'game', 'game_image': '3516_Final_Fantasy_V.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 1, 'comp_lvl_mp': 1, 'comp_lvl_spd': 1, 'comp_main': 116278, 'comp_plus': 133771, 'comp_100': 232940, 'comp_all': 133006, 'comp_main_count': 201, 'comp_plus_count': 251, 'comp_100_count': 52, 'comp_all_count': 504, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 1023, 'count_speedrun': 3, 'count_backlog': 2223, 'count_review': 394, 'review_score': 79, 'count_playing': 29, 'count_retired': 90, 'profile_dev': 'Square', 'profile_popular': 160, 'profile_steam': 1173810, 'profile_platform': 'Game Boy Advance, Mobile, PC, PlayStation, PlayStation Portable, Super Nintendo', 'release_world': 1992}, {'count': 7, 'game_id': 3499, 'game_name': 'Final Fantasy IV', 'game_name_date': 1, 'game_alias': 'Final Fantasy II [NA], Final Fantasy 4, FF4, Final Fantasy IV: Pixel Remaster', 'game_type': 'game', 'game_image': 'Final_Fantasy_IV.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_lvl_spd': 1, 'comp_main': 79723, 'comp_plus': 95438, 'comp_100': 132860, 'comp_all': 91532, 'comp_main_count': 198, 'comp_plus_count': 255, 'comp_100_count': 66, 'comp_all_count': 519, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 1164, 'count_speedrun': 2, 'count_backlog': 1379, 'count_review': 455, 'review_score': 79, 'count_playing': 15, 'count_retired': 69, 'profile_dev': 'Square', 'profile_popular': 160, 'profile_steam': 1173800, 'profile_platform': 'Game Boy Advance, Mobile, PC, PlayStation, PlayStation Portable, Super Nintendo, WonderSwan', 'release_world': 1991}, {'count': 7, 'game_id': 3495, 'game_name': 'Final Fantasy II', 'game_name_date': 0, 'game_alias': 'Final Fantasy 2, FF2, Final Fantasy II: Pixel Remaster', 'game_type': 'game', 'game_image': '250px-Ff2cover.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_lvl_spd': 1, 'comp_main': 86695, 'comp_plus': 108067, 'comp_100': 114410, 'comp_all': 96309, 'comp_main_count': 281, 'comp_plus_count': 174, 'comp_100_count': 94, 'comp_all_count': 549, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 1001, 'count_speedrun': 1, 'count_backlog': 1107, 'count_review': 429, 'review_score': 62, 'count_playing': 12, 'count_retired': 91, 'profile_dev': 'Square', 'profile_popular': 156, 'profile_steam': 1173780, 'profile_platform': 'Game Boy Advance, Mobile, NES, PC, PlayStation, PlayStation Portable, WonderSwan', 'release_world': 1988}, {'count': 7, 'game_id': 94537, 'game_name': 'Final Fantasy III', 'game_name_date': 1, 'game_alias': 'Final Fantasy 3 (Original), Final Fantasy III: Pixel Remaster', 'game_type': 'game', 'game_image': '250px-Ff3cover.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_lvl_spd': 1, 'comp_main': 66808, 'comp_plus': 71988, 'comp_100': 82640, 'comp_all': 74192, 'comp_main_count': 47, 'comp_plus_count': 59, 'comp_100_count': 49, 'comp_all_count': 155, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 281, 'count_speedrun': 0, 'count_backlog': 383, 'count_review': 119, 'review_score': 74, 'count_playing': 9, 'count_retired': 10, 'profile_dev': 'SquareSoft', 'profile_popular': 101, 'profile_steam': 1173790, 'profile_platform': 'Mobile, NES, PC', 'release_world': 1990}], 'displayModifier': None}

    game = Game.parse(
        data=result['data'][0]
    )
    print(game)
    # Game(id=3505, title='Final Fantasy IX', aliases=['Final Fantasy 9', 'FF9'], duration_main_seconds=139631, duration_main_title='38:47:11', duration_plus_seconds=191277, duration_plus_title='53:07:57', duration_100_seconds=293791, duration_100_title='81:36:31', duration_all_seconds=172652, duration_all_title='47:57:32', release_world=2000, profile_platforms=['Mobile', 'Nintendo Switch', 'PC', 'PlayStation', 'PlayStation 4', 'Xbox One'])
