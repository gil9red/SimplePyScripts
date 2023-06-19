#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math

import requests
from bs4 import BeautifulSoup


def decrypt_phone(clipped_phone, value):
    decrypt = value / 17

    p1 = int(math.floor(decrypt / 100))
    p2 = int(decrypt - 100 * p1)
    t1 = str(p1)[1:] + "-" + str(p2).zfill(2)

    return clipped_phone.replace("...", "") + t1


def get_phone(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "lxml")

    button_show_phone = root.select_one("#show-phone_button")
    blst = int(button_show_phone["blst"])
    lst1 = int(button_show_phone["lst1"])
    lst2 = int(button_show_phone["lst2"])

    phones = list()

    for phone_tag in root.select(".object-builder-phone"):
        if phone_tag.has_attr("blst") and phone_tag["blst"] == "true":
            value = blst

        elif phone_tag.has_attr("lst1") and phone_tag["lst1"] == "true":
            value = lst1

        elif phone_tag.has_attr("lst2") and phone_tag["lst2"] == "true":
            value = lst2

        else:
            raise Exception(
                'Отсутствует один из атрибутов: blst, lst1, lst2, или значение не "true"'
            )

        phone = decrypt_phone(phone_tag.text, value)
        phones.append(phone)

    return phones


if __name__ == "__main__":
    print(get_phone("http://www.realestate.ru/flatrent/4274613/"))
    print(get_phone("http://www.realestate.ru/retailrent/176651/"))
    print(get_phone("http://www.realestate.ru/retailrent/180232/"))
