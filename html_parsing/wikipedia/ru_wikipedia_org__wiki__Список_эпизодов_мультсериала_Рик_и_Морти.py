#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def get_seasons() -> dict[str, list[str]]:
    url = "https://ru.wikipedia.org/wiki/Список_эпизодов_мультсериала_«Рик_и_Морти»"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    season_by_series = dict()

    for season_title_el in root.select('span[id ^= "Сезон"]'):
        season_title = season_title_el.text

        # "Сезон 6 (2022)" -> "Сезон 6"
        season_title = re.sub(r"\(.+\)", "", season_title).strip()

        table_series = season_title_el.parent.find_next_sibling(
            "table", attrs={"class": "wikitable"}
        )
        if not table_series:
            continue

        series_list = []
        for title_el in table_series.select("tr td.summary b"):
            # Удаление сносок, типа "«Солярикс[en]»"
            if sup_el := title_el.find("sup"):
                sup_el.decompose()

            series_title = title_el.get_text(strip=True)
            series_list.append(series_title)

        assert series_list, f"Не найдена ни одна серия! Сезон: {season_title}"
        season_by_series[season_title] = series_list

    return season_by_series


def get_all_series() -> list[str]:
    return [
        f"{season}. {series}"
        for season, series_list in get_seasons().items()
        for series in series_list
    ]



if __name__ == "__main__":
    season_by_series = get_seasons()
    for season, series_list in season_by_series.items():
        print(f"{season} ({len(series_list)}):")
        for series in series_list:
            print(f"    {series}")

        print()

    print("\n" + "-" * 10 + "\n")

    all_series = get_all_series()
    print(f"All series ({len(all_series)}): {all_series}")
