#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import NamedTuple

import requests
from bs4 import BeautifulSoup, Tag


class Achievement(NamedTuple):
    title: str
    description: str
    img_url: str

    @staticmethod
    def from_node(achieve_node: Tag) -> "Achievement":
        achieve_txt_node = achieve_node.select_one(".achieveTxt")
        title = achieve_txt_node.h3.text.strip()
        description = achieve_txt_node.h5.text.strip()

        img_url = achieve_node.select_one(".achieveImgHolder > img")["src"]

        return Achievement(title, description, img_url)


def get_achievements(game_id: int) -> list[Achievement]:
    url = f"https://steamcommunity.com/stats/{game_id}/achievements"

    headers = {
        # Чтобы описание было на русском, без этого заголовка описание будет на английском
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    rs = requests.get(url, headers=headers)
    root = BeautifulSoup(rs.content, "html.parser")

    return [Achievement.from_node(x) for x in root.select(".achieveRow")]


if __name__ == "__main__":
    game_id = 426790
    achievements = get_achievements(game_id)
    print(achievements[0]._asdict())
    print(f"{len(achievements)}: {achievements}")
    print([x.title for x in achievements])
    print()

    # Print and export
    all_achievements = []

    game_id_name_list = [
        (426790, "Grow Up"),
        (489830, "The Elder Scrolls V: Skyrim Special Edition"),
        ("L4D2", "Left 4 Dead 2"),
        (582010, "MONSTER HUNTER: WORLD"),
        (374320, "DARK SOULS™ III"),
        (292030, "The Witcher® 3: Wild Hunt"),
        (418370, "Resident Evil 7: Biohazard"),
    ]
    for game_id, name in game_id_name_list:
        achievements = get_achievements(game_id)
        titles = [x.title for x in achievements]
        print(f"{name} ({len(titles)}): {titles}")

        all_achievements.append(
            {
                "name": name,
                "id": game_id,
                "achievements": [x._asdict() for x in achievements],
            }
        )

    import json

    with open("steam_achievements.json", "w", encoding="utf-8") as f:
        json.dump(all_achievements, f, ensure_ascii=False, indent=4)
