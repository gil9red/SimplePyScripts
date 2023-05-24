#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


PATTERN_PARSE = re.compile(
    r"пол: (\w+).*национальность: (\w+).*дата рождения: (\d{1,2}\.\d{1,2}\.\d{4})"
)

rs = requests.get("https://мвд.рф/wanted")

# NOTE: Monkey patch for attribute href: <a class="e-popup_html" href="#popup-33644" href="#">
content = rs.content.replace(b' href="#"', b"")

root = BeautifulSoup(content, "html.parser")
items = root.select(".sl-item-title > a")

for i, a in enumerate(items, 1):
    name = a.text
    print(f"{i:2}. {name}")

    detail_text = root.select_one(a["href"] + " .sd-text").get_text(strip=True)
    m = PATTERN_PARSE.search(detail_text)
    if m:
        sex, nationality, date_of_birth = m.groups()
        print(
            f"    Пол: {sex}, национальность: {nationality}, дата рождения: {date_of_birth}"
        )
    else:
        print("    <не получилось распарсить>")
        print(detail_text)

    print()

#  1. ЕРМОЛИНСКИЙ СЕМЕН АЛЕКСЕЕВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 16.3.1987
#
#  2. КИРИЛЛОВ ВЛАДИМИР ИЛЬИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 31.5.1956
#
#  3. МАМОНОВ ДМИТРИЙ ЕВГЕНЬЕВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 3.10.1981
#
#  4. ЕМЕЛЬЯНОВ НИКОЛАЙ ВИКТОРОВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 18.9.1961
#
#  5. САМОЙЛОВ АНДРЕЙ АНДРЕЕВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 28.11.1969
#
#  6. ТИМОШЕНКО ОЛЕГ ЕВГЕНЬЕВИЧ
#     Пол: МУЖ, национальность: УКРАИНЕЦ, дата рождения: 10.1.1967
#
#  7. МАХМУДОВ ФАХРУДИН АЛИБЕГОВИЧ
#     Пол: МУЖ, национальность: ДАГЕСТАНЕЦ, дата рождения: 13.12.1965
#
#  8. ЧЕКИН ЮРИЙ ВАСИЛЬЕВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 1.1.1963
#
#  9. АНДРЕЕВ ВАЛЕРИЙ НИКОЛАЕВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 10.4.1957
#
# 10. ШЕСТЕРИН ВЛАДИМИР ВИКТОРОВИЧ
#     Пол: МУЖ, национальность: РУССКИЙ, дата рождения: 18.8.1977
