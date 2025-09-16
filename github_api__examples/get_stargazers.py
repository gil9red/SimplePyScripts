#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import User, get_users


def get_stargazers(owner: str, repository: str) -> list[User]:
    url: str = f"https://api.github.com/repos/{owner}/{repository}/stargazers"
    return get_users(url)


if __name__ == "__main__":
    users: list[User] = get_stargazers("gil9red", "SimplePyScripts")
    print(f"Stargazers ({len(users)}):")
    print(*users[:5], sep="\n")
    print("...")
    print(*users[-5:], sep="\n")
    """
    Stargazers (153):
    User(login='numb7', url='https://github.com/numb7')
    User(login='Martin-Winter', url='https://github.com/Martin-Winter')
    User(login='Shaar68', url='https://github.com/Shaar68')
    User(login='triplekill', url='https://github.com/triplekill')
    User(login='JMSwag', url='https://github.com/JMSwag')
    ...
    User(login='bobophp', url='https://github.com/bobophp')
    User(login='emnioj', url='https://github.com/emnioj')
    User(login='Wisepal61', url='https://github.com/Wisepal61')
    User(login='Codycode91', url='https://github.com/Codycode91')
    User(login='jellykioto', url='https://github.com/jellykioto')
    """
