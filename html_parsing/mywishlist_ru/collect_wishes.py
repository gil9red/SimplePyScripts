#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import time

from pathlib import Path

from get_wish_info import Wish
from get_last_id_wish import get_last_id_wish


DIR = Path(__file__).resolve().parent
FILE_NAME_DUMP = DIR / "dump.json"


def run():
    wish_id = 1
    last_id_wish = get_last_id_wish()

    if FILE_NAME_DUMP.exists():
        with open(FILE_NAME_DUMP, encoding="utf-8") as f:
            items = json.load(f)
        wish_id = max(items, key=lambda x: x["id"])["id"] + 1
    else:
        items = []

    while wish_id < last_id_wish:
        print(f"#{wish_id}")

        try:
            wish = Wish.parse_from(wish_id)
            if wish:
                items.append(wish.as_dict())
                with open(FILE_NAME_DUMP, "w", encoding="utf-8") as f:
                    json.dump(items, f, ensure_ascii=False, indent=4)
            else:
                print(f"#{wish_id} не найдено!")

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)
            continue

        wish_id += 1
        time.sleep(1)

        # Достигли максимального известного id - попробуем его обновить
        if wish_id == last_id_wish:
            last_id_wish = get_last_id_wish()


if __name__ == "__main__":
    run()
