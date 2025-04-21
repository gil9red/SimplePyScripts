#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
from common import session


def get_seasons() -> dict[str, list[str]]:
    url = "https://ru.wikipedia.org/wiki/Список_эпизодов_мультсериала_«Футурама»"

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    season_by_series: dict[str, list[str]] = dict()

    for season_title_el in soup.select('h3[id ^= "Сезон"]'):
        season_title = season_title_el.get_text(strip=True)

        table_series = season_title_el.parent.find_next_sibling(
            "table", attrs={"class": "wikitable"}
        )
        if not table_series:
            continue

        series_list = []
        for title_el in table_series.select("tr td.summary > b"):
            # Удаление сносок
            for sub in title_el.select("sup"):
                sub.decompose()

            series_title = title_el.get_text(strip=True)
            series_list.append(series_title)

        season_by_series[season_title] = series_list

    assert season_by_series, "Не найден ни один сезон!"

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
