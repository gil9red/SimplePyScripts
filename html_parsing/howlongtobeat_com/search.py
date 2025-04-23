#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from urllib.parse import urljoin
from typing import Any

from common import URL_BASE, session, Game


def api_search(text: str, page: int = 1) -> dict[str, Any]:
    url_first = f"{URL_BASE}/?q={text}"

    rs = session.get(url_first)
    rs.raise_for_status()

    m = re.search(r'<script src="([\w/]+_app-[\w/]+\.js)"', rs.text)
    if not m:
        raise Exception("<script> не найдено!")

    url_js: str = urljoin(URL_BASE, m.group(1))

    rs = session.get(url_js)
    rs.raise_for_status()

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
                "rangeTime": {"min": None, "max": None},
                "gameplay": {
                    "difficulty": "",
                    "perspective": "",
                    "flow": "",
                    "genre": "",
                    "subGenre": " ",
                },
                "rangeYear": {"min": "", "max": ""},
                "modifier": "",
            },
            "users": {"sortCategory": "postcount"},
            "lists": {"sortCategory": "follows"},
            "filter": "",
            "sort": 0,
            "randomizer": 0,
        },
        "useCache": True,
    }

    text_js: str = rs.text

    m_uri_api_search = re.search("/api/(search|find|lookup|s|ouch|seek)/", text_js)
    if m_uri_api_search:
        uri_api_search = m_uri_api_search.group()
    else:
        raise Exception("Не найден URI api search!")

    url_api_search = f"{URL_BASE}{uri_api_search}"

    # NOTE: fetch("/api/search/".concat("foo").concat("bar"),
    #       fetch("/api/search/".concat("foobar"),
    m_concat_search_key = re.search(rf'"{uri_api_search}"(.+?),', text_js)
    if m_concat_search_key:
        concat_search_key = m_concat_search_key.group(1)

        # NOTE: .concat("foo").concat("bar") -> "foobar"
        #       .concat("foobar") -> "foobar"
        search_key = "".join(
            m.group(1) for m in re.finditer(r""""(\w+)"|'(\w+)'""", concat_search_key)
        )
        url_api_search = f"{url_api_search}/{search_key}"

    m_search_user_id = re.search(r',users:\{id:"([a-zA-Z0-9]+)",', text_js)
    if m_search_user_id:
        search_user_id = m_search_user_id.group(1)
        data["searchOptions"]["users"]["id"] = search_user_id

    for k in ["subGenre", "difficulty"]:
        m_k = re.search(r"""{f}:['"](.*?)['"]""", text_js)
        if m_k:
            data["searchOptions"]["games"]["gameplay"][k] = m_k.group(1)

    rs = session.post(
        url_api_search,
        headers={"Referer": url_first},
        json=data,
    )
    rs.raise_for_status()

    return rs.json()


# TODO: def search(text: str) -> list[Game]:


if __name__ == "__main__":
    text = "Final Fantasy IX"
    result = api_search(text)
    print("Result:", result)
    # Result: {'color': 'blue', 'title': '', 'category': 'games', 'count': 7, 'pageCurrent': 1, 'pageTotal': 1, 'pageSize': 20, 'data': [{'game_id': 3505, 'game_name': 'Final Fantasy IX', 'game_name_date': 0, 'game_alias': 'Final Fantasy 9, FF9', 'game_type': 'game', 'game_image': '3505_Final_Fantasy_IX.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 137551, 'comp_plus': 189596, 'comp_100': 296245, 'comp_all': 171497, 'comp_main_count': 852, 'comp_plus_count': 821, 'comp_100_count': 203, 'comp_all_count': 1876, 'invested_co': 216000, 'invested_mp': 0, 'invested_co_count': 1, 'invested_mp_count': 0, 'count_comp': 4711, 'count_speedrun': 7, 'count_backlog': 7504, 'count_review': 1591, 'review_score': 88, 'count_playing': 74, 'count_retired': 294, 'profile_popular': 371, 'release_world': 2000}, {'game_id': 3519, 'game_name': 'Final Fantasy VI', 'game_name_date': 0, 'game_alias': 'Final Fantasy III [NA], Final Fantasy 3 [NA], Final Fantasy 6, FF6, Final Fantasy VI Advance, Final Fantasy VI: Pixel Remaster', 'game_type': 'game', 'game_image': '3519_Final_Fantasy_VI.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 122768, 'comp_plus': 146578, 'comp_100': 213056, 'comp_all': 147082, 'comp_main_count': 364, 'comp_plus_count': 728, 'comp_100_count': 191, 'comp_all_count': 1283, 'invested_co': 198990, 'invested_mp': 0, 'invested_co_count': 2, 'invested_mp_count': 0, 'count_comp': 3094, 'count_speedrun': 3, 'count_backlog': 5882, 'count_review': 1167, 'review_score': 88, 'count_playing': 71, 'count_retired': 277, 'profile_popular': 375, 'release_world': 1994}, {'game_id': 3480, 'game_name': 'Final Fantasy', 'game_name_date': 0, 'game_alias': 'Final Fantasy 1, FF1, Final Fantasy: Pixel Remaster', 'game_type': 'game', 'game_image': '3480_Final_Fantasy.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 56488, 'comp_plus': 66841, 'comp_100': 70629, 'comp_all': 63319, 'comp_main_count': 826, 'comp_plus_count': 639, 'comp_100_count': 595, 'comp_all_count': 2060, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 4090, 'count_speedrun': 4, 'count_backlog': 2375, 'count_review': 1485, 'review_score': 72, 'count_playing': 55, 'count_retired': 193, 'profile_popular': 313, 'release_world': 1987}, {'game_id': 3495, 'game_name': 'Final Fantasy II', 'game_name_date': 0, 'game_alias': 'Final Fantasy 2, FF2, Final Fantasy II: Pixel Remaster', 'game_type': 'game', 'game_image': '3495_Final_Fantasy_II.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 78539, 'comp_plus': 90927, 'comp_100': 96532, 'comp_all': 86374, 'comp_main_count': 461, 'comp_plus_count': 296, 'comp_100_count': 254, 'comp_all_count': 1011, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 2007, 'count_speedrun': 1, 'count_backlog': 2222, 'count_review': 793, 'review_score': 64, 'count_playing': 39, 'count_retired': 135, 'profile_popular': 257, 'release_world': 1988}, {'game_id': 3516, 'game_name': 'Final Fantasy V', 'game_name_date': 0, 'game_alias': 'Final Fantasy 5, FF5, Final Fantasy V: Pixel Remaster', 'game_type': 'game', 'game_image': '3516_Final_Fantasy_V.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 114179, 'comp_plus': 130598, 'comp_100': 202135, 'comp_all': 131974, 'comp_main_count': 275, 'comp_plus_count': 390, 'comp_100_count': 110, 'comp_all_count': 775, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 1718, 'count_speedrun': 3, 'count_backlog': 3767, 'count_review': 644, 'review_score': 80, 'count_playing': 41, 'count_retired': 146, 'profile_popular': 252, 'release_world': 1992}, {'game_id': 3499, 'game_name': 'Final Fantasy IV', 'game_name_date': 1, 'game_alias': 'Final Fantasy II [NA], Final Fantasy 4, FF4, Final Fantasy IV: Pixel Remaster', 'game_type': 'game', 'game_image': '3499_Final_Fantasy_IV.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 73475, 'comp_plus': 86695, 'comp_100': 98460, 'comp_all': 84594, 'comp_main_count': 340, 'comp_plus_count': 387, 'comp_100_count': 187, 'comp_all_count': 914, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 2051, 'count_speedrun': 2, 'count_backlog': 2555, 'count_review': 766, 'review_score': 80, 'count_playing': 43, 'count_retired': 109, 'profile_popular': 219, 'release_world': 1991}, {'game_id': 94537, 'game_name': 'Final Fantasy III', 'game_name_date': 1, 'game_alias': 'Final Fantasy 3 (Original), Final Fantasy III: Pixel Remaster', 'game_type': 'game', 'game_image': '94537_Final_Fantasy_III.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 59622, 'comp_plus': 68007, 'comp_100': 69169, 'comp_all': 65513, 'comp_main_count': 151, 'comp_plus_count': 161, 'comp_100_count': 177, 'comp_all_count': 489, 'invested_co': 0, 'invested_mp': 0, 'invested_co_count': 0, 'invested_mp_count': 0, 'count_comp': 939, 'count_speedrun': 0, 'count_backlog': 1447, 'count_review': 385, 'review_score': 74, 'count_playing': 25, 'count_retired': 25, 'profile_popular': 181, 'release_world': 1990}], 'userData': [], 'displayModifier': None}

    result_data = result["data"][0]
    print("Result data:", result_data)
    # Result data: {'game_id': 3505, 'game_name': 'Final Fantasy IX', 'game_name_date': 0, 'game_alias': 'Final Fantasy 9, FF9', 'game_type': 'game', 'game_image': '3505_Final_Fantasy_IX.jpg', 'comp_lvl_combine': 0, 'comp_lvl_sp': 1, 'comp_lvl_co': 0, 'comp_lvl_mp': 0, 'comp_main': 137551, 'comp_plus': 189935, 'comp_100': 295568, 'comp_all': 171560, 'comp_main_count': 852, 'comp_plus_count': 823, 'comp_100_count': 204, 'comp_all_count': 1879, 'invested_co': 216000, 'invested_mp': 0, 'invested_co_count': 1, 'invested_mp_count': 0, 'count_comp': 4728, 'count_speedrun': 7, 'count_backlog': 7542, 'count_review': 1600, 'review_score': 88, 'count_playing': 78, 'count_retired': 302, 'profile_platform': 'Mobile, Nintendo Switch, PC, PlayStation, PlayStation 4, Xbox One', 'profile_popular': 403, 'release_world': 2000}

    game = Game.parse(data=result_data)
    print(game)
    # Game(id=3505, title='Final Fantasy IX', aliases=['Final Fantasy 9', 'FF9'], duration_main_seconds=137551, duration_main_title='38:12:31', duration_plus_seconds=189596, duration_plus_title='52:39:56', duration_100_seconds=296245, duration_100_title='82:17:25', duration_all_seconds=171497, duration_all_title='47:38:17', release_world=2000, profile_platforms=[''], profile_genres=[''])

    assert "Final Fantasy IX" == game.title
