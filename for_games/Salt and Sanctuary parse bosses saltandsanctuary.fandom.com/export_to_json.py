#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import json

from utils import get_bosses, convert_bosses_to_only_name


def export_to_json_str(bosses: dict[str, list[str]]) -> str:
    return json.dumps(bosses, ensure_ascii=False, indent=4)


def export_to_json(file_name: str, bosses: dict[str, list[str]]):
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)

    json.dump(
        bosses,
        open(file_name, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


if __name__ == "__main__":
    bosses = get_bosses()
    bosses_only_names = convert_bosses_to_only_name(bosses)

    print(export_to_json_str(bosses_only_names))
    # {
    #     "Обязательные боссы": [
    #         "Обезумевший рыцарь",
    #         "Краекан циклоп",
    #         "Безумный алхимик",
    #         "Фальшивый шут",
    #         "Краекан вирм",
    #         "Нетронутый инквизитор",
    #         "Третий агнец",
    #         "Иссушенный король",
    #         "Ведьма озера",
    #         "Бескожий и Архитектор",
    #         "Краекан дракон Скоурж",
    #         "Безымянный бог"
    #     ],
    #     "Опциональные боссы": [
    #         "Немая бездна",
    #         "Королева улыбок",
    #         "Древо людей",
    #         "Выпотрошенная оболочка",
    #         "Отвратительный смрад",
    #         "Кран Ронин",
    #         "Мёрдиела Мол",
    #         "Бескровный принц",
    #         "Жаждущий",
    #         "Карсджоу Жестокий",
    #         "Забытый король"
    #     ]
    # }

    export_to_json("dumps/bosses.json", bosses)
    export_to_json("dumps/bosses__only_name.json", bosses_only_names)
