#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def clear_text(el) -> str:
    if el is None:
        return ""

    return el.get_text(strip=True)


def get_html() -> BeautifulSoup:
    rs = requests.get("https://www.worldometers.info/coronavirus/")
    return BeautifulSoup(rs.content, "html.parser")


def _get_tr_data(tr_el) -> dict[str, str]:
    [
        _,
        total_cases,
        new_cases,
        total_deaths,
        new_deaths,
        total_recovered,
        active_cases,
        serious,
        tot_cases,
    ] = map(clear_text, tr_el.select("td"))

    return {
        "total_cases": total_cases,
        "new_cases": new_cases,
        "total_deaths": total_deaths,
        "new_deaths": new_deaths,
        "total_recovered": total_recovered,
        "active_cases": active_cases,
        "serious": serious,
        "tot_cases": tot_cases,
    }


def get_total_statistics() -> dict[str, str]:
    root = get_html()

    tr = root.select_one("#main_table_countries_today > tbody > tr.total_row")
    return _get_tr_data(tr)


def get_all() -> dict[str, dict[str, str]]:
    root = get_html()

    data = dict()

    for tr in root.select("#main_table_countries_today > tbody > tr"):
        country = clear_text(tr.select("td")[0])
        if country in ["Diamond Princess", "Total:"]:
            continue

        data[country] = _get_tr_data(tr)

    return data


if __name__ == "__main__":
    print(get_total_statistics())
    # {'total_cases': '226,470', 'new_cases': '7,682', 'total_deaths': '9,285', 'new_deaths': '342',
    #  'total_recovered': '85,831', 'active_cases': '131,354', 'serious': '6,896', 'tot_cases': '29.1'}

    print()

    data = get_all()
    print(data)
    # {'China': {'total_cases': '80,928', 'new_cases': '+34', 'total_deaths': '3,245', 'new_deaths': '+8', ...

    print(data["Russia"])
    # {'total_cases': '199', 'new_cases': '+52', 'total_deaths': '1', 'new_deaths': '+1',
    #  'total_recovered': '8', 'active_cases': '190', 'serious': '', 'tot_cases': '1'}
