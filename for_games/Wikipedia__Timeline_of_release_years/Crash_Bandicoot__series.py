#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_parsed_two_column_wikitable() -> list[tuple[str, str]]:
    url = "https://en.wikipedia.org/wiki/Crash_Bandicoot"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    table = root.select_one(".wikitable.release-timeline")

    items = []
    year = None

    # Timeline of release years
    for tr in table.select("tr"):
        # Отбрасываем строки с годом, но без игры
        if tr.td is None:
            continue

        if tr.th and tr.td:
            year = tr.th.text.strip()
            name = tr.td.i.text.strip()

        else:
            # Сюда попадают игры, попавшие с другими в один и тот же год, например
            #     2000: Resident Evil Survivor
            #     2000: Resident Evil – Code: Veronica
            #
            # year берется из предыдущей строки
            # year = ...
            name = tr.td.i.text.strip()

        if year and name:
            items.append((year, name))

    return items


if __name__ == "__main__":
    for year, name in get_parsed_two_column_wikitable():
        print(f"{year}: {name}")

    # 1996: Crash Bandicoot
    # 1997: Cortex Strikes Back
    # 1998: Warped
    # 1999: Crash Team Racing
    # 2000: Crash Bash
    # 2001: Wrath of Cortex
    # 2002: The Huge Adventure
    # 2003: N-Tranced
    # 2003: Crash Nitro Kart
    # 2004: Purple: Ripto's Rampage
    # 2004: Twinsanity
    # 2005: Crash Tag Team Racing
    # 2006: Crash Boom Bang!
    # 2007: Crash of the Titans
    # 2008: Mind over Mutant
    # 2008: Nitro Kart 3D
    # 2009: Mutant Island
    # 2010: Nitro Kart 2
    # 2017: N. Sane Trilogy
    # 2019: Crash Team Racing Nitro-Fueled
    # 2020: Crash Bandicoot Mobile
    # 2020: It's About Time
