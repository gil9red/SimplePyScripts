#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def get_user_rank_and_reputation() -> tuple[str, str]:
    url = "https://stackexchange.com/leagues/filter-users/609/AllTime/2015-03-27/?filter=gil9red&sort=reputationchange"

    rs = requests.get(url)
    text = rs.text
    # print(text)

    match = re.search(">#(.+)</span> all time rank", text)
    rank = match.group(1)

    match = re.search(">(.+)</span> all time reputation", text)
    reputation = match.group(1).replace(",", "")

    return rank, reputation


if __name__ == "__main__":
    rank, reputation = get_user_rank_and_reputation()
    print("rank:", rank)
    print("reputation:", reputation)
