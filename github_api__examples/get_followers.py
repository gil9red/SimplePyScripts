#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from common import User


def get_followers(owner: str) -> list[User]:
    url = f"https://api.github.com/users/{owner}/followers"

    per_page = 100
    page = 1

    items = []

    while True:
        params = dict(per_page=per_page, page=page)
        rs = requests.get(url, params=params)
        rs.raise_for_status()

        result: list[dict] = rs.json()
        if not result:
            break

        items += [
            User(
                login=item["login"],
                url=item["html_url"],
            )
            for item in result
        ]

        page += 1

    return items


if __name__ == "__main__":
    users = get_followers("gil9red")
    print(f"Followers ({len(users)}):")
    print(*users[:5], sep="\n")
    print("...")
    print(*users[-5:], sep="\n")
    """
    Followers (92):
    User(login='shakshin', url='https://github.com/shakshin')
    User(login='AgelxNash', url='https://github.com/AgelxNash')
    User(login='insolor', url='https://github.com/insolor')
    User(login='suconakh', url='https://github.com/suconakh')
    User(login='oldkiller', url='https://github.com/oldkiller')
    ...
    User(login='Alexwhite2007', url='https://github.com/Alexwhite2007')
    User(login='SPSEBASTIAAN', url='https://github.com/SPSEBASTIAAN')
    User(login='ali-lipi', url='https://github.com/ali-lipi')
    User(login='Alimkh85', url='https://github.com/Alimkh85')
    User(login='barb455555', url='https://github.com/barb455555')
    """
