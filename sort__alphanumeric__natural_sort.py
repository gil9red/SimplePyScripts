#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def get_num(text: str) -> int:
    return int("".join(filter(str.isdigit, text)))


def natural_sorted(items: list) -> list:
    return sorted(items, key=get_num)


def natural_sort(items: list):
    items.sort(key=get_num)


if __name__ == "__main__":
    items = [
        "_img_1.png",
        "_img_10.png",
        "_img_11.png",
        "_img_12.png",
        "_img_13.png",
        "_img_14.png",
        "_img_15.png",
        "_img_16.png",
        "_img_17.png",
        "_img_18.png",
        "_img_19.png",
        "_img_2.png",
        "_img_20.png",
        "_img_21.png",
        "_img_22.png",
        "_img_23.png",
        "_img_24.png",
        "_img_25.png",
        "_img_26.png",
        "_img_3.png",
        "_img_4.png",
        "_img_5.png",
        "_img_6.png",
        "_img_7.png",
        "_img_8.png",
        "_img_9.png",
    ]
    print(sorted(items))
    # ['_img_1.png', '_img_10.png', '_img_11.png', '_img_12.png', ...
    print()

    print(natural_sorted(items))
    # ['_img_1.png', '_img_2.png', '_img_3.png', '_img_4.png', '_img_5.png', ...

    natural_sort(items)
    print(items)
    # ['_img_1.png', '_img_2.png', '_img_3.png', '_img_4.png', '_img_5.png', ...
