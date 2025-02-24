#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random


def get_random_rarity_item():
    a = random.randrange(1, 1000)

    if a <= 10:
        return "легендарный"
    elif a <= 100:
        return "эпический"
    elif a <= 250:
        return "редкий"
    else:
        return "обычный"


if __name__ == "__main__":
    print(get_random_rarity_item())
    print(get_random_rarity_item())
    print(get_random_rarity_item())
