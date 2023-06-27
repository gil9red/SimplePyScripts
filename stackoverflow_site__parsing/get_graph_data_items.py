#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def get_graph_data_items(url: str) -> list:
    rs = requests.get(url)

    # EXAMPLE: var graphData = [937,937,937,937,937,935,935,935,935,935 ...];
    match = re.search(r"var graphData\s*=\s*\[([\d,]+?)\];", rs.text)
    if not match:
        print('Not found "var graphData = [...];"')
        return []

    return match.group(1).split(",")


if __name__ == "__main__":
    url = "https://ru.stackoverflow.com/users/201445/gil9red?tab=reputation"
    items = get_graph_data_items(url)
    print(f"Items ({len(items)}): {items}")

    items.reverse()

    print(f"Items ({len(items)}): {items}")
    print("Last 5:", items[:5])
