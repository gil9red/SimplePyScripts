#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from typing import List


def get_tracked_products() -> List[dict]:
    return json.load(open("tracked_products.json", encoding="utf-8"))
