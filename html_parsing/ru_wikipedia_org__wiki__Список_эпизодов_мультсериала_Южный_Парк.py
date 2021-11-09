#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def get_seasons() -> Dict[str, List[str]]:
    url = 'https://ru.wikipedia.org/wiki/Список_эпизодов_мультсериала_«Южный_Парк»'

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    season_by_series = dict()

    for season_title_el in root.select('span[id ^= "Сезон"]'):
        season_title = season_title_el.get_text(strip=True)

        table_series = season_title_el.parent.find_next_sibling('table', attrs={'class': 'wikitable'})
        assert table_series, 'Не найдена таблица серий!'

        series_list = []
        for tr in table_series.select('tr:has(td)'):
            td_list = tr.select('td')
            td_list_count = len(td_list)

            if td_list_count == 4:  # Old version
                series_title = td_list[0].select_one('b > a').get_text(strip=True)
                series_list.append(series_title)

            elif td_list_count > 4:  # New version
                series_title = td_list[2].select_one('b > a').get_text(strip=True)
                series_list.append(series_title)

        assert series_list, f'Не найдена ни одна серия! Сезон: {season_title}'
        season_by_series[season_title] = series_list

    return season_by_series


def get_all_series() -> List[str]:
    return [
        f'{season}. {series}'
        for season, series_list in get_seasons().items()
        for series in series_list
    ]


if __name__ == '__main__':
    season_by_series = get_seasons()
    for season, series_list in season_by_series.items():
        print(f'{season} ({len(series_list)}):')
        for series in series_list:
            print(f'    {series}')

        print()

    print('\n' + '-' * 10 + '\n')

    all_series = get_all_series()
    print(f'All series ({len(all_series)}): {all_series}')
