#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from common import User


def get_stargazers(owner: str, repository: str) -> list[User]:
    url = f"https://api.github.com/repos/{owner}/{repository}/stargazers"

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
    users = get_stargazers("gil9red", "SimplePyScripts")
    print(f"Stargazers ({len(users)}):")
    print(*users[:5], sep="\n")
    print("...")
    print(*users[-5:], sep="\n")
    """
    Stargazers (148):
    User(login='numb7', url='https://github.com/numb7')
    User(login='Martin-Winter', url='https://github.com/Martin-Winter')
    User(login='Shaar68', url='https://github.com/Shaar68')
    User(login='triplekill', url='https://github.com/triplekill')
    User(login='JMSwag', url='https://github.com/JMSwag')
    ...
    User(login='Aarab228', url='https://github.com/Aarab228')
    User(login='jjh4568520', url='https://github.com/jjh4568520')
    User(login='eplord', url='https://github.com/eplord')
    User(login='EzzalddeenAli', url='https://github.com/EzzalddeenAli')
    User(login='techbrain19', url='https://github.com/techbrain19')
    """
