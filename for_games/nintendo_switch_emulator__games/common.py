#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from pathlib import Path


def get_json_file_name(file_name: str) -> str:
    return Path(file_name).name + ".json"


def dump(file_name: str, games: list, playable_games: list, perfect_games: list) -> None:
    data = {
        "perfect_games": {
            "total": len(perfect_games),
            "items": perfect_games,
        },
        "playable_games": {
            "total": len(playable_games),
            "items": playable_games,
        },
        "games": {
            "total": len(games),
            "items": games,
        },
    }
    json.dump(
        data,
        open(file_name, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
