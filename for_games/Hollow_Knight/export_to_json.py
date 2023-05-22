#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import json

from utils import Boss, get_bosses, convert_bosses_to_only_name


def export_to_json_str(bosses: dict[str, list]) -> str:
    return json.dumps(bosses, ensure_ascii=False, indent=4)


def export_to_json(file_name: str, bosses: dict[str, list]):
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)

    json.dump(
        bosses, open(file_name, "w", encoding="utf-8"), ensure_ascii=False, indent=4
    )


if __name__ == "__main__":
    bosses: dict[str, list[Boss]] = get_bosses()
    bosses_only_names: dict[str, list[str]] = convert_bosses_to_only_name(bosses)

    print(export_to_json_str(bosses_only_names))
    """
    {
        "Боссы": [
            "Матка Жужж",
            "Ложный Рыцарь/Сломленный чемпион",
            "Задумчивый чревень",
            "Закруглан",
            "Воин душ",
            "Король мстекрылов",
            "Разбитый Сосуд/Потерянный собрат",
            "Кристаллический страж",
            "Навозный защитник",
            "Тремоматка",
            "Божья укротительница",
            "Полый рыцарь",
            "Хорнет",
            "Лорды богомолов",
            "Носк",
            "Мастер душ/Душегуб",
            "Коллекционер",
            "Лучезарность",
            "Предавший лорд",
            "Ууму",
            "Рыцарь-хранитель",
            "Серый принц Зот",
            "Белый защитник",
            "Гримм",
            "Король кошмара",
            "Рыцарь Улья",
            "Мастера гвоздя Оро и Мато",
            "Мастер кисти Шео",
            "Великий гуру гвоздей Слай",
            "Боевые сёстры",
            "Крылатый Носк",
            "Чистый Сосуд",
            "Всевышняя Лучезарность"
        ],
        "Воины грёз": [
            "Старейшина Ху",
            "Гальен",
            "Горб",
            "Маркот",
            "Марму",
            "Незрячая",
            "Ксеро"
        ]
    }
    """

    export_to_json("dumps/bosses.json", bosses)
    export_to_json("dumps/bosses__only_name.json", bosses_only_names)
