#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_inherited_children(url, root):
    td_inherited_by = None

    for x in root.select(".alignedsummary td"):
        if x.text.strip() == "Inherited By:":
            td_inherited_by = x
            break

    if not td_inherited_by:
        # print('Not found "Inherited By:" td.')
        return []

    td_list = td_inherited_by.find_next_sibling("td").select("a")
    return [(a.text.strip(), urljoin(url, a["href"])) for a in td_list]


def print_children(url, total_class_list, global_number=-1, indent_level=0):
    if global_number > 0 and len(total_class_list) >= global_number:
        # print('GLOBAL_NUMBER!')
        return

    time.sleep(1)

    indent = "  " * indent_level

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    name_class = root.select_one(".context > .title").text.split()[0]
    total_class_list.append(name_class)

    inherited_children = get_inherited_children(url, root)
    number_inherited_children = len(inherited_children)
    if number_inherited_children > 0:
        print(indent + "{} ({}):".format(name_class, number_inherited_children))
    else:
        print(indent + name_class)

    for name, url in inherited_children:
        print_children(url, total_class_list, global_number, indent_level + 1)


ROOT_URL = "http://doc.qt.io/qt-5/qobject.html"


if __name__ == "__main__":
    global_number = -1
    total_class_list = []

    print_children(ROOT_URL, total_class_list, global_number)

    import json
    json.dump(
        total_class_list,
        open("total_class.json", "w", encoding="utf-8"),
        ensure_ascii=False,
    )
