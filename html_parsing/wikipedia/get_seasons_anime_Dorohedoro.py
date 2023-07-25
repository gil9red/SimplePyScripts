#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def get_seasons() -> list[str]:
    rs = requests.get("https://en.wikipedia.org/wiki/List_of_Dorohedoro_episodes")
    rs.raise_for_status()

    items = re.findall(r"Season \w+", rs.text, flags=re.IGNORECASE)
    return sorted(set(items))


if __name__ == "__main__":
    print(get_seasons())
    # ['Season One']
