#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import sys
from collections import defaultdict

from main import FILE_NAME_DUMP, get_vk_session


if not FILE_NAME_DUMP.exists():
    print(f"Файл {FILE_NAME_DUMP.name!r} не найден, попробуй запустить main.py")
    sys.exit()

vk_session = get_vk_session()
vk = vk_session.get_api()

dump = json.load(open(FILE_NAME_DUMP, encoding="utf-8"))

current_id_by_names = defaultdict(set)
for x in dump:
    for author in x["authors"]:
        author_id = author["id"]
        name = author["name"]
        current_id_by_names[author_id].add(name)

# Поиск измененных авторов
new_id_by_name = dict()
for author_id, authors in current_id_by_names.items():
    names = ", ".join(map(repr, authors))

    rs = vk.users.get(user_ids=author_id)[0]
    name = f"{rs['first_name']} {rs['last_name']}".strip()

    # Если текущее имя не в списке имен или в списке имен их несколько
    if (name not in authors or len(authors) > 1) and "DELETED" not in name:
        print(
            f"Актуализация имени {name!r} у пользователя с id={author_id}, предыдущие имена: {names}"
        )
        new_id_by_name[author_id] = name
        continue

    # Если сейчас пользователь удален и в дампе есть несколько его имен
    if "DELETED" in name and len(authors) > 1:
        name = sorted(authors)[-1]
        print(
            f"В настоящий момент пользователь удален. Актуализация имени {name!r} "
            f"у пользователя с id={author_id}, из предыдущих имен: {names}"
        )
        new_id_by_name[author_id] = name

if new_id_by_name:
    print("Дамп нужно обновить")

    for x in dump:
        for author in x["authors"]:
            author_id = author["id"]
            if author_id in new_id_by_name:
                author["name"] = new_id_by_name[author_id]

    json.dump(
        dump,
        open(FILE_NAME_DUMP, "w", encoding="utf-8"),
        indent=4,
        ensure_ascii=False,
    )
else:
    print("Дамп обновлять не нужно")
