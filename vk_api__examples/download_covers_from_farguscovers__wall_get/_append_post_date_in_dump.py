#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import json
import sys
from collections import defaultdict

from main import FILE_NAME_DUMP, get_wall_it


if not FILE_NAME_DUMP.exists():
    print(f"Файл {FILE_NAME_DUMP.name!r} не найден, попробуй запустить main.py")
    sys.exit()

dump = json.load(open(FILE_NAME_DUMP, encoding="utf-8"))

id_by_dumps = defaultdict(list)
for x in dump:
    post_id = x["post_id"]
    id_by_dumps[post_id].append(x)

for post in get_wall_it():
    post_id = post["id"]
    if post_id not in id_by_dumps:
        continue

    date_time = dt.datetime.fromtimestamp(post["date"])

    for x in id_by_dumps[post_id]:
        x["date_time"] = str(date_time)

print("Дамп перезаписан")

json.dump(
    dump,
    open(FILE_NAME_DUMP, "w", encoding="utf-8"),
    indent=4,
    ensure_ascii=False,
)
