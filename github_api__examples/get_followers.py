#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import User, get_users


def get_followers(owner: str) -> list[User]:
    url: str = f"https://api.github.com/users/{owner}/followers"
    return get_users(url)


if __name__ == "__main__":
    users: list[User] = get_followers("gil9red")
    print(f"Followers ({len(users)}):")
    print(*users[:5], sep="\n")
    print("...")
    print(*users[-5:], sep="\n")
    """
    Followers (98):
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
