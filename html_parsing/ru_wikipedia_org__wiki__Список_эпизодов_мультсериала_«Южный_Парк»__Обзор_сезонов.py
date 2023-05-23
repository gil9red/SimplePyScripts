#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


def parse_date(date_str: str) -> DT.date:
    """
    Example: "20 января 1999"
    """

    day, month, year = date_str.split()
    day = int(day)
    month = [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ].index(month) + 1
    year = int(year)

    return DT.date(year, month, day)


@dataclass
class Season:
    season: int
    num_episodes: int
    start_date: DT.date
    end_date: DT.date
    diff_dates: DT.timedelta


def parse() -> list[Season]:
    url = "https://ru.wikipedia.org/wiki/Список_эпизодов_мультсериала_«Южный_Парк»"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    items = []
    for tr in root.select_one(".wikitable").select("tr"):
        td_list = tr.select("td")
        if len(td_list) != 4:
            continue

        td_season, td_num_episodes, td_start_date, td_end_date = td_list

        season = int(td_season.get_text(strip=True))
        num_episodes = int(td_num_episodes.get_text(strip=True))
        start_date = parse_date(
            " ".join(a.get_text(strip=True) for a in td_start_date.select("a"))
        )
        end_date = parse_date(
            " ".join(a.get_text(strip=True) for a in td_end_date.select("a"))
        )

        items.append(
            Season(season, num_episodes, start_date, end_date, end_date - start_date)
        )

    return items


if __name__ == "__main__":
    import sys

    sys.path.append("..")
    from ascii_table__simple_pretty__format import print_pretty_table

    seasons = parse()
    print("Total seasons:", len(seasons))
    print("Total episodes:", sum(s.num_episodes for s in seasons))
    print()
    # Total seasons: 23
    # Total episodes: 307

    rows = [("СЕЗОН", "ЭПИЗОДЫ", "НАЧАЛО ЭФИРА", "КОНЕЦ ЭФИРА", "ДНЕЙ ЭФИРА")]
    for s in seasons:
        rows.append((
            s.season,
            s.num_episodes,
            s.start_date.strftime("%d/%m/%Y"),
            s.end_date.strftime("%d/%m/%Y"),
            s.diff_dates.days,
        ))

    print_pretty_table(rows)

    # СЕЗОН | ЭПИЗОДЫ | НАЧАЛО ЭФИРА | КОНЕЦ ЭФИРА | ДНЕЙ ЭФИРА
    # ------+---------+--------------+-------------+-----------
    #     1 |      13 |   13/08/1997 |  25/02/1998 |        196
    #     2 |      18 |   01/04/1998 |  20/01/1999 |        294
    #     3 |      17 |   07/04/1999 |  12/01/2000 |        280
    #     4 |      17 |   05/04/2000 |  20/12/2000 |        259
    #     5 |      14 |   20/06/2001 |  12/12/2001 |        175
    #     6 |      17 |   06/03/2002 |  11/12/2002 |        280
    #     7 |      15 |   19/03/2003 |  17/12/2003 |        273
    #     8 |      14 |   17/03/2004 |  15/12/2004 |        273
    #     9 |      14 |   09/03/2005 |  07/12/2005 |        273
    #    10 |      14 |   22/03/2006 |  15/11/2006 |        238
    #    11 |      14 |   07/03/2007 |  14/11/2007 |        252
    #    12 |      14 |   12/03/2008 |  19/11/2008 |        252
    #    13 |      14 |   11/03/2009 |  18/11/2009 |        252
    #    14 |      14 |   17/03/2010 |  17/11/2010 |        245
    #    15 |      14 |   27/04/2011 |  16/11/2011 |        203
    #    16 |      14 |   14/03/2012 |  07/11/2012 |        238
    #    17 |      10 |   25/09/2013 |  11/12/2013 |         77
    #    18 |      10 |   24/09/2014 |  10/12/2014 |         77
    #    19 |      10 |   16/09/2015 |  09/12/2015 |         84
    #    20 |      10 |   14/09/2016 |  07/12/2016 |         84
    #    21 |      10 |   13/09/2017 |  06/12/2017 |         84
    #    22 |      10 |   26/09/2018 |  12/12/2018 |         77
    #    23 |      10 |   25/09/2019 |  11/12/2019 |         77
