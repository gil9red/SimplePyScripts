#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
from typing import Any, Self

import requests


@dataclass
class LatestReport:
    os: str
    tested_date: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(os=data["os"], tested_date=data["testedDate"])


@dataclass
class Game:
    key: str
    title: str
    title_id: str
    overall: str
    os: dict[str, str]
    report_counts: dict[str, int]
    latest_tested: str
    report_revision: str
    latest_report: LatestReport
    screenshots: list[str] = field(default_factory=list)
    all_title_ids: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            title=data["title"],
            title_id=data["titleId"],
            overall=data["overall"],
            os=data["os"],
            report_counts=data["reportCounts"],
            latest_tested=data["latestTested"],
            report_revision=data["reportRevision"],
            latest_report=LatestReport.from_dict(data["latestReport"]),
            screenshots=data["screenshots"],
            all_title_ids=data["allTitleIds"],
            aliases=data["aliases"],
        )


URL: str = "https://kytyps5.github.io/data/compat-index.json"


def get_compatibility() -> list[Game]:
    rs = requests.get(URL)
    rs.raise_for_status()

    data: dict[str, Any] = rs.json()
    if not data.get("games"):
        raise Exception("No games found")

    return [Game.from_dict(game_data) for game_data in data["games"]]


if __name__ == "__main__":
    games: list[Game] = get_compatibility()
    print(f"Total: {len(games)}")
    print(*games[:5], sep="\n")
    print("...")
    print(*games[-5:], sep="\n")
    """
    Total: 379
    Game(key='PPSA24249', title='1348 Ex Voto', title_id='PPSA24249', overall='main-menu', os={'windows': 'main-menu'}, report_counts={'windows': 1}, latest_tested='2026-10-18', report_revision='48c47d2ec4d971f5', latest_report=LatestReport(os='windows', tested_date='2026-10-18'), screenshots=[], all_title_ids=['PPSA24249', 'PPSA33621'], aliases=['1348-ex-voto-windows'])
    Game(key='PPSA02800', title='3D Billiards - Pool & Snooker', title_id='PPSA02800', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-07-22', report_revision='44e4e54a38e3d509', latest_report=LatestReport(os='windows', tested_date='2026-07-22'), screenshots=[], all_title_ids=['PPSA02799', 'PPSA02800'], aliases=['3d-billiards-windows'])
    Game(key='PPSA03647', title='3D MiniGolf - Makeover-Edition', title_id='PPSA03647', overall='in-game', os={'windows': 'in-game', 'linux': 'in-game'}, report_counts={'windows': 1, 'linux': 1}, latest_tested='2026-09-25', report_revision='8b2477df43eca833', latest_report=LatestReport(os='linux', tested_date='2026-09-25'), screenshots=[], all_title_ids=['PPSA03646', 'PPSA03647', 'PPSA26878', 'PPSA26940'], aliases=['3d-mini-golf-linux', '3d-mini-golf-windows'])
    Game(key='PPSA04583', title='41 Hours', title_id='PPSA04583', overall='doesnt-boot', os={'windows': 'doesnt-boot'}, report_counts={'windows': 1}, latest_tested='2026-08-31', report_revision='d245fc178c85ffeb', latest_report=LatestReport(os='windows', tested_date='2026-08-31'), screenshots=[{'title': '41 Hours', 'screenshot': 'https://github.com/user-attachments/assets/a5768d14-5974-4a2a-a107-81fb721a274d', 'testedDate': '2026-08-31', 'os': 'windows'}, {'title': '41 Hours', 'screenshot': 'https://github.com/user-attachments/assets/856f7f43-3ab5-45db-8739-de6a1f415c0b', 'testedDate': '2026-08-31', 'os': 'windows'}], all_title_ids=['PPSA04583', 'PPSA04584'], aliases=['41-hours-windows'])
    Game(key='PPSA05265', title='A Memoir Blue', title_id='PPSA05265', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-17', report_revision='9853f5e1e1dd5e9f', latest_report=LatestReport(os='windows', tested_date='2026-10-17'), screenshots=[{'title': 'A Memoir Blue', 'screenshot': 'https://github.com/user-attachments/assets/356970a4-6e03-44db-ac15-0e4b300b1bf3', 'testedDate': '2026-10-17', 'os': 'windows'}, {'title': 'A Memoir Blue', 'screenshot': 'https://github.com/user-attachments/assets/972944e4-1119-446a-a990-60e4934da0c5', 'testedDate': '2026-10-17', 'os': 'windows'}], all_title_ids=['PPSA05265', 'PPSA05266', 'PPSA05267', 'PPSA05268'], aliases=['a-memoir-blue-windows'])
    ...
    Game(key='PPSA34299', title='WWE 2K26', title_id='PPSA34299', overall='doesnt-boot', os={'windows': 'doesnt-boot'}, report_counts={'windows': 1}, latest_tested='2026-10-09', report_revision='defeccaa9d47e523', latest_report=LatestReport(os='windows', tested_date='2026-10-09'), screenshots=[], all_title_ids=['PPSA34299'], aliases=['wwe-2k26-windows'])
    Game(key='PPSA02775', title='XIII', title_id='PPSA02775', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-09-15', report_revision='c43ce35ea6c36456', latest_report=LatestReport(os='windows', tested_date='2026-09-15'), screenshots=[{'title': 'XIII', 'screenshot': 'https://github.com/user-attachments/assets/1ebcac2c-16cd-4169-9c80-8b6e7c3eaab1', 'testedDate': '2026-09-15', 'os': 'windows'}], all_title_ids=['PPSA02774', 'PPSA02775'], aliases=['xiii-windows'])
    Game(key='PPSA32456', title='Ys X: Proud Nordics', title_id='PPSA32456', overall='logo', os={'windows': 'logo'}, report_counts={'windows': 1}, latest_tested='2026-08-29', report_revision='5f037dd77882fe83', latest_report=LatestReport(os='windows', tested_date='2026-08-29'), screenshots=[], all_title_ids=['PPSA32456', 'PPSA32457'], aliases=['ys-x-proud-nordics-windows'])
    Game(key='PPSA22624', title='Zombie Cure Lab', title_id='PPSA22624', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-08', report_revision='a605cf82986cb916', latest_report=LatestReport(os='windows', tested_date='2026-10-08'), screenshots=[{'title': 'Zombie Cure Lab', 'screenshot': 'https://github.com/user-attachments/assets/2166cdc5-89c8-4238-badb-fd46c2f19c21', 'testedDate': '2026-10-08', 'os': 'windows'}, {'title': 'Zombie Cure Lab', 'screenshot': 'https://github.com/user-attachments/assets/f99e4a73-d784-430c-b187-d3e3e82f5a7a', 'testedDate': '2026-10-08', 'os': 'windows'}], all_title_ids=['PPSA22623', 'PPSA22624'], aliases=['zombie-cure-lab-windows'])
    Game(key='PPSA33096', title='メモリーズオフ 双想 ～Break out of my shell～', title_id='PPSA33096', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-08-28', report_revision='caf7232680ec0d76', latest_report=LatestReport(os='windows', tested_date='2026-08-28'), screenshots=[], all_title_ids=['PPSA33096', 'PPSA35400'], aliases=['memories-off-sousou-break-out-of-my-shell-windows'])
    """

    print("\n" + "-" * 100 + "\n")

    from collections import Counter

    os_by_number: Counter[str] = Counter()
    os_state_by_number: Counter[str] = Counter()
    state_by_number: Counter[str] = Counter()

    for game in games:
        for os, state in game.os.items():
            os_by_number[os] += 1
            os_state_by_number[f"{os}+{state}"] += 1
            state_by_number[state] += 1

    print("Stats:")
    print(f"OS:         {dict(os_by_number.most_common())}")
    print(f"OS + state: {dict(os_state_by_number.most_common())}")
    print(f"State:      {dict(state_by_number.most_common())}")
    """
    Stats:
    OS:         {'windows': 351, 'linux': 51, 'macos': 3}
    OS + state: {'windows+in-game': 188, 'windows+logo': 60, 'windows+main-menu': 56, 'windows+doesnt-boot': 47, 'linux+in-game': 32, 'linux+logo': 8, 'linux+doesnt-boot': 6, 'linux+main-menu': 5, 'macos+doesnt-boot': 3}
    State:      {'in-game': 220, 'logo': 68, 'main-menu': 61, 'doesnt-boot': 56}
    """

    # TODO: Вывести определенные игры: Demon's Souls, Astro Bot, Gran Turismo 7 (Gran Turismo™ 7)

    print("\n" + "-" * 100 + "\n")

    TARGET_GAMES: list[str] = [
        "Demon's Souls",
        "Astro Bot",
        "Gran Turismo 7",
    ]

    import re

    # NOTE: https://github.com/gil9red/SimplePyScripts/blob/3eca1c95e5fb15684a75d20c8d1142a1c3e1698e/video_parsers/youtube/search_video_in_channels.py#L16-L26
    def smart_comparing(game_name: str, playlist_title: str) -> bool:
        # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/55b3256c9cfaf338ef0e055c08d8d60720c66c79/html_parsing/get_game_genres/common.py#L31
        def clear_name(name: str) -> str:
            return re.sub(r"\W", "", name)

        clear_game_name = clear_name(game_name).lower()
        clear_playlist_title = clear_name(playlist_title).lower()
        return (
            clear_game_name in clear_playlist_title
            or clear_playlist_title in clear_game_name
        )

    for game in games:
        if any(smart_comparing(game.title, name) for name in TARGET_GAMES):
            print(game)
    """
    Game(key='PPSA21564', title='ASTRO BOT', title_id='PPSA21564', overall='in-game', os={'windows': 'in-game', 'linux': 'in-game', 'macos': 'doesnt-boot'}, report_counts={'windows': 1, 'linux': 1, 'macos': 1}, latest_tested='2026-10-28', report_revision='f53045348098276f', latest_report=LatestReport(os='windows', tested_date='2026-10-28'), screenshots=[{'title': 'ASTRO BOT', 'screenshot': 'https://github.com/user-attachments/assets/054b8fd0-49f6-44f3-bb69-a4a4f250a0ad', 'testedDate': '2026-10-02', 'os': 'linux'}, {'title': 'ASTRO BOT', 'screenshot': 'https://github.com/user-attachments/assets/30f7eb21-9913-4b91-a9f7-0ddc8eacc0b1', 'testedDate': '2026-10-02', 'os': 'linux'}, {'title': 'ASTRO BOT', 'screenshot': 'https://github.com/user-attachments/assets/c8abca24-6fe3-41d4-a383-cc8363580c6b', 'testedDate': '2026-10-02', 'os': 'linux'}, {'title': 'ASTRO BOT', 'screenshot': 'https://github.com/user-attachments/assets/0a11bd6e-1c17-47fb-9737-62ae3514a628', 'testedDate': '2026-10-02', 'os': 'linux'}], all_title_ids=['PPSA21559', 'PPSA21564', 'PPSA21567', 'PPSA21568', 'PPSA23060', 'PPSA23687'], aliases=['astro-bot-windows', 'astro-bot-macos', 'astro-bot-linux'])
    Game(key='PPSA01342', title="Demon's Souls", title_id='PPSA01342', overall='main-menu', os={'windows': 'main-menu', 'linux': 'logo'}, report_counts={'windows': 1, 'linux': 1}, latest_tested='2026-10-26', report_revision='dfea0b4373d04eec', latest_report=LatestReport(os='linux', tested_date='2026-10-26'), screenshots=[], all_title_ids=['PPSA01339', 'PPSA01340', 'PPSA01341', 'PPSA01342', 'PPSA01678', 'PPSA01689', 'PPSA01690', 'PPSA01691'], aliases=['demon-souls-linux', 'demon-s-souls-windows'])
    Game(key='PPSA01317', title='Gran Turismo™ 7', title_id='PPSA01317', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-09', report_revision='893cd2380d1f09a3', latest_report=LatestReport(os='windows', tested_date='2026-10-09'), screenshots=[], all_title_ids=['PPSA01315', 'PPSA01316', 'PPSA01317', 'PPSA01318', 'PPSA05483', 'PPSA05484', 'PPSA05485', 'PPSA05486'], aliases=['gran-turismo-7-windows'])    
    """
