#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import gettext

# pip install pycountry
import pycountry

russian = gettext.translation("iso3166", pycountry.LOCALES_DIR, languages=["ru"])
russian.install()


def get_country(code):
    ru = pycountry.countries.get(alpha_2=code)
    return _(ru.name)


if __name__ == "__main__":
    print(get_country("RU"))
    # Российская Федерация

    print(get_country("US"))
    # Соединённые штаты

    print(get_country("DE"))
    # Германия

    print(get_country("CA"))
    # Канада

    print(get_country("FR"))
    # Франция
