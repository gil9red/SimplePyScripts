#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import generate
from ds2_locations import get_graph


FILE_NAME = "ds2_locations.html"


if __name__ == "__main__":
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        g = get_graph()
        text = generate(g)
        f.write(text)
