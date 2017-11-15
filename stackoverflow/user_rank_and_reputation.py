#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_user_rank_and_reputation() -> (str, str):
    url = 'https://stackexchange.com/leagues/filter-users/355/AllTime/2015-03-27/?filter=gil9red&sort=reputationchange'

    import requests
    rs = requests.get(url)
    text = rs.text
    # print(text)

    import re
    match = re.search('>#(.+)</span> all time rank', text)
    rank = match.group(1)

    match = re.search('>(.+)</span> all time reputation', text)
    reputation = match.group(1).replace(',', '')

    return rank, reputation


if __name__ == '__main__':
    rank, reputation = get_user_rank_and_reputation()
    print('rank:', rank)
    print('reputation:', reputation)
