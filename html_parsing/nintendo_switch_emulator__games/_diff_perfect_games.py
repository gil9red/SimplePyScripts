#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import common


ryujinx_games = json.load(open("ryujinx.py.json", encoding="utf-8"))
yuzu_games = json.load(open("yuzu.py.json", encoding="utf-8"))

ryujinx_perfect_games = set(ryujinx_games["perfect_games"]["items"])
yuzu_perfect_games = set(yuzu_games["perfect_games"]["items"])

common_games = sorted(ryujinx_perfect_games & yuzu_perfect_games)
print("commons:", len(common_games), common_games)
# Commons: 25 ...

only_ryujinx_perfect_games = sorted(ryujinx_perfect_games - yuzu_perfect_games)
print(
    "only_ryujinx_perfect_games:",
    len(only_ryujinx_perfect_games),
    only_ryujinx_perfect_games,
)

only_yuzu_perfect_games = sorted(yuzu_perfect_games - ryujinx_perfect_games)
print("only_yuzu_perfect_games:", len(only_yuzu_perfect_games), only_yuzu_perfect_games)

# Dump
data = {
    "common_games": {
        "total": len(common_games),
        "items": common_games,
    },
    "only_ryujinx_games": {
        "total": len(only_ryujinx_perfect_games),
        "items": only_ryujinx_perfect_games,
    },
    "only_yuzu_games": {
        "total": len(only_yuzu_perfect_games),
        "items": only_yuzu_perfect_games,
    },
}

file_name = common.get_json_file_name(__file__)
json.dump(
    data,
    open(file_name, "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)
