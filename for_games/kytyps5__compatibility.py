#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Self

import requests

HOST: str = "https://kytyps5.github.io"
URL: str = f"{HOST}/data/compat-index.json"


@dataclass
class LatestReport:
    os: str
    tested_date: date

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            os=data["os"],
            tested_date=date.fromisoformat(data["testedDate"]),
        )


@dataclass
class Screenshot:
    title: str
    screenshot: str
    os: str
    tested_date: date

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            title=data["title"],
            screenshot=data["screenshot"],
            os=data["os"],
            tested_date=date.fromisoformat(data["testedDate"]),
        )


@dataclass
class Game:
    key: str
    title: str
    title_id: str
    overall: str
    os: dict[str, str]
    report_counts: dict[str, int]
    latest_tested: date
    report_revision: str
    latest_report: LatestReport
    screenshots: list[Screenshot] = field(default_factory=list)
    all_title_ids: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"{HOST}/game/{self.key}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            title=data["title"],
            title_id=data["titleId"],
            overall=data["overall"],
            os=data["os"],
            report_counts=data["reportCounts"],
            latest_tested=date.fromisoformat(data["latestTested"]),
            report_revision=data["reportRevision"],
            latest_report=LatestReport.from_dict(data["latestReport"]),
            screenshots=[
                Screenshot.from_dict(screenshot) for screenshot in data["screenshots"]
            ],
            all_title_ids=data["allTitleIds"],
            aliases=data["aliases"],
        )


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


def get_compatibility(filters: list[str] | None = None) -> list[Game]:
    rs = requests.get(URL)
    rs.raise_for_status()

    data: dict[str, Any] = rs.json()
    if not data.get("games"):
        raise Exception("No games found")

    games = [Game.from_dict(game_data) for game_data in data["games"]]
    if filters:
        games = [
            game
            for game in games
            if any(smart_comparing(game.title, name) for name in filters)
        ]

    return games


if __name__ == "__main__":
    games: list[Game] = get_compatibility()
    print(f"Total: {len(games)}")
    print(*games[:5], sep="\n")
    print("...")
    print(*games[-5:], sep="\n")
    """
    Total: 414
    Game(key='PPSA11386', title='007 First Light', title_id='PPSA11386', overall='doesnt-boot', os={'windows': 'doesnt-boot'}, report_counts={'windows': 1}, latest_tested='2026-10-30', report_revision='62dde303bf642637', latest_report=LatestReport(os='windows', tested_date='2026-10-30'), screenshots=[{'title': '007 First Light', 'screenshot': 'https://github.com/user-attachments/assets/4f242ee2-c26b-437b-9962-2d02be554f7c', 'testedDate': '2026-10-30', 'os': 'windows'}], all_title_ids=['PPSA11386'], aliases=['007-first-light-1-018-000-windows'])
    Game(key='PPSA24249', title='1348 Ex Voto', title_id='PPSA24249', overall='main-menu', os={'windows': 'main-menu'}, report_counts={'windows': 1}, latest_tested='2026-10-18', report_revision='48c47d2ec4d971f5', latest_report=LatestReport(os='windows', tested_date='2026-10-18'), screenshots=[], all_title_ids=['PPSA24249', 'PPSA33621'], aliases=['1348-ex-voto-windows'])
    Game(key='PPSA02800', title='3D Billiards - Pool & Snooker', title_id='PPSA02800', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-07-22', report_revision='44e4e54a38e3d509', latest_report=LatestReport(os='windows', tested_date='2026-07-22'), screenshots=[], all_title_ids=['PPSA02799', 'PPSA02800'], aliases=['3d-billiards-windows'])
    Game(key='PPSA03647', title='3D MiniGolf - Makeover-Edition', title_id='PPSA03647', overall='in-game', os={'windows': 'in-game', 'linux': 'in-game'}, report_counts={'windows': 1, 'linux': 1}, latest_tested='2026-09-25', report_revision='8b2477df43eca833', latest_report=LatestReport(os='linux', tested_date='2026-09-25'), screenshots=[], all_title_ids=['PPSA03646', 'PPSA03647', 'PPSA26878', 'PPSA26940'], aliases=['3d-mini-golf-linux', '3d-mini-golf-windows'])
    Game(key='PPSA04583', title='41 Hours', title_id='PPSA04583', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-30', report_revision='9162cdc1e04efe08', latest_report=LatestReport(os='windows', tested_date='2026-10-30'), screenshots=[{'title': '41 Hours', 'screenshot': 'https://github.com/user-attachments/assets/d88430a4-76d2-4211-ac72-64ebcccb5257', 'testedDate': '2026-10-30', 'os': 'windows'}, {'title': '41 Hours', 'screenshot': 'https://github.com/user-attachments/assets/05dcc1a5-972d-438a-a1ca-84af94265a33', 'testedDate': '2026-10-30', 'os': 'windows'}, {'title': '41 Hours', 'screenshot': 'https://github.com/user-attachments/assets/1597c618-b648-4bab-bb28-f0190fa22f1a', 'testedDate': '2026-10-30', 'os': 'windows'}], all_title_ids=['PPSA04583', 'PPSA04584'], aliases=['41-hours-windows'])
    ...
    Game(key='PPSA09546', title='You Suck at Parking®', title_id='PPSA09546', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-19', report_revision='8685f1be66f4dc5e', latest_report=LatestReport(os='windows', tested_date='2026-10-19'), screenshots=[{'title': 'You Suck at Parking®', 'screenshot': 'https://github.com/user-attachments/assets/1fb4e4a1-0705-40f3-8bcb-5d5f2f39efce', 'testedDate': '2026-10-19', 'os': 'windows'}, {'title': 'You Suck at Parking®', 'screenshot': 'https://github.com/user-attachments/assets/72411144-c79f-408d-ae2f-55acba38597d', 'testedDate': '2026-10-19', 'os': 'windows'}, {'title': 'You Suck at Parking®', 'screenshot': 'https://github.com/user-attachments/assets/19c2cf2e-d390-410d-9163-019eeebae1b7', 'testedDate': '2026-10-19', 'os': 'windows'}, {'title': 'You Suck at Parking®', 'screenshot': 'https://github.com/user-attachments/assets/767a09dc-129c-497f-b726-888c311752f7', 'testedDate': '2026-10-19', 'os': 'windows'}, {'title': 'You Suck at Parking®', 'screenshot': 'https://github.com/user-attachments/assets/21bad2c6-f3d7-405c-9e98-9d3beac4e7a7', 'testedDate': '2026-10-19', 'os': 'windows'}, {'title': 'You Suck at Parking®', 'screenshot': 'https://github.com/user-attachments/assets/37e46efa-5684-4e0d-8b24-ccf753cb1835', 'testedDate': '2026-10-19', 'os': 'windows'}], all_title_ids=['PPSA08894', 'PPSA09546', 'PPSA11026', 'PPSA11027', 'PPSA13220', 'PPSA13224'], aliases=['you-suck-at-parking-windows'])
    Game(key='PPSA32456', title='Ys X: Proud Nordics', title_id='PPSA32456', overall='logo', os={'windows': 'logo'}, report_counts={'windows': 1}, latest_tested='2026-08-29', report_revision='5f037dd77882fe83', latest_report=LatestReport(os='windows', tested_date='2026-08-29'), screenshots=[], all_title_ids=['PPSA32456', 'PPSA32457'], aliases=['ys-x-proud-nordics-windows'])
    Game(key='PPSA22624', title='Zombie Cure Lab', title_id='PPSA22624', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-08', report_revision='a605cf82986cb916', latest_report=LatestReport(os='windows', tested_date='2026-10-08'), screenshots=[{'title': 'Zombie Cure Lab', 'screenshot': 'https://github.com/user-attachments/assets/2166cdc5-89c8-4238-badb-fd46c2f19c21', 'testedDate': '2026-10-08', 'os': 'windows'}, {'title': 'Zombie Cure Lab', 'screenshot': 'https://github.com/user-attachments/assets/f99e4a73-d784-430c-b187-d3e3e82f5a7a', 'testedDate': '2026-10-08', 'os': 'windows'}], all_title_ids=['PPSA22623', 'PPSA22624'], aliases=['zombie-cure-lab-windows'])
    Game(key='PPSA33802', title='マイリトルパピー', title_id='PPSA33802', overall='in-game', os={'windows': 'in-game'}, report_counts={'windows': 1}, latest_tested='2026-10-15', report_revision='6a4b4d8dec59ad5a', latest_report=LatestReport(os='windows', tested_date='2026-10-15'), screenshots=[{'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/e634d2e1-ceac-4d37-823c-f3b87bed077b', 'testedDate': '2026-10-15', 'os': 'windows'}, {'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/888e39b5-410b-4762-adf4-07b8cc09ce1c', 'testedDate': '2026-10-15', 'os': 'windows'}, {'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/f3de2775-998d-463d-87af-e6b27636f79b', 'testedDate': '2026-10-15', 'os': 'windows'}, {'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/98d24f50-ddf0-42b4-abe9-1b2f09796784', 'testedDate': '2026-10-15', 'os': 'windows'}, {'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/8221d6c7-9c6e-4bf7-9ded-8b8340577d2e', 'testedDate': '2026-10-15', 'os': 'windows'}, {'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/821b44cd-8348-4146-982e-c5d068ddfa91', 'testedDate': '2026-10-15', 'os': 'windows'}, {'title': 'マイリトルパピー', 'screenshot': 'https://github.com/user-attachments/assets/bf79e66a-057c-49bc-bd01-b79203c732cd', 'testedDate': '2026-10-15', 'os': 'windows'}], all_title_ids=['PPSA33802'], aliases=['my-little-puppy-windows'])
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
    OS:         {'windows': 386, 'linux': 54, 'macos': 3}
    OS + state: {'windows+in-game': 214, 'windows+main-menu': 62, 'windows+logo': 61, 'windows+doesnt-boot': 49, 'linux+in-game': 34, 'linux+logo': 9, 'linux+doesnt-boot': 6, 'linux+main-menu': 5, 'macos+doesnt-boot': 3}
    State:      {'in-game': 248, 'logo': 70, 'main-menu': 67, 'doesnt-boot': 58}
    """

    print("\n" + "-" * 100 + "\n")

    TARGET_GAMES: list[str] = [
        "Demon's Souls",
        "Astro Bot",
        "Gran Turismo 7",
    ]
    for game in get_compatibility(filters=TARGET_GAMES):
        print(game)

        lines: list[str] = [
            game.title,
            "OS:",
            "\n".join(f"    {os.title()}: {stat}" for os, stat in game.os.items()),
            f"Latest Tested: {game.latest_tested}",
            f"Url: {game.url}",
        ]
        print("\n".join(lines))
        print()
    """
    Game(key='PPSA21564', title='ASTRO BOT', title_id='PPSA21564', overall='in-game', os={'windows': 'in-game', 'linux': 'in-game', 'macos': 'doesnt-boot'}, report_counts={'windows': 1, 'linux': 1, 'macos': 1}, latest_tested=datetime.date(2026, 10, 28), report_revision='f53045348098276f', latest_report=LatestReport(os='windows', tested_date=datetime.date(2026, 10, 28)), screenshots=[Screenshot(title='ASTRO BOT', screenshot='https://github.com/user-attachments/assets/054b8fd0-49f6-44f3-bb69-a4a4f250a0ad', os='linux', tested_date=datetime.date(2026, 10, 2)), Screenshot(title='ASTRO BOT', screenshot='https://github.com/user-attachments/assets/30f7eb21-9913-4b91-a9f7-0ddc8eacc0b1', os='linux', tested_date=datetime.date(2026, 10, 2)), Screenshot(title='ASTRO BOT', screenshot='https://github.com/user-attachments/assets/c8abca24-6fe3-41d4-a383-cc8363580c6b', os='linux', tested_date=datetime.date(2026, 10, 2)), Screenshot(title='ASTRO BOT', screenshot='https://github.com/user-attachments/assets/0a11bd6e-1c17-47fb-9737-62ae3514a628', os='linux', tested_date=datetime.date(2026, 10, 2))], all_title_ids=['PPSA21559', 'PPSA21564', 'PPSA21567', 'PPSA21568', 'PPSA23060', 'PPSA23687'], aliases=['astro-bot-windows', 'astro-bot-macos', 'astro-bot-linux'])
    ASTRO BOT
    OS:
        Windows: in-game
        Linux: in-game
        Macos: doesnt-boot
    Latest Tested: 2026-10-28
    Url: https://kytyps5.github.io/game/PPSA21564
    
    Game(key='PPSA01342', title="Demon's Souls", title_id='PPSA01342', overall='main-menu', os={'windows': 'main-menu', 'linux': 'logo'}, report_counts={'windows': 1, 'linux': 1}, latest_tested=datetime.date(2026, 10, 26), report_revision='dfea0b4373d04eec', latest_report=LatestReport(os='linux', tested_date=datetime.date(2026, 10, 26)), screenshots=[], all_title_ids=['PPSA01339', 'PPSA01340', 'PPSA01341', 'PPSA01342', 'PPSA01678', 'PPSA01689', 'PPSA01690', 'PPSA01691'], aliases=['demon-souls-linux', 'demon-s-souls-windows'])
    Demon's Souls
    OS:
        Windows: main-menu
        Linux: logo
    Latest Tested: 2026-10-26
    Url: https://kytyps5.github.io/game/PPSA01342
    
    Game(key='PPSA01317', title='Gran Turismo™ 7', title_id='PPSA01317', overall='in-game', os={'windows': 'in-game', 'linux': 'logo'}, report_counts={'windows': 1, 'linux': 1}, latest_tested=datetime.date(2026, 10, 27), report_revision='523f997e15cfc7fe', latest_report=LatestReport(os='linux', tested_date=datetime.date(2026, 10, 27)), screenshots=[], all_title_ids=['PPSA01315', 'PPSA01316', 'PPSA01317', 'PPSA01318', 'PPSA05483', 'PPSA05484', 'PPSA05485', 'PPSA05486'], aliases=['gran-turismo-7-linux', 'gran-turismo-7-windows'])
    Gran Turismo™ 7
    OS:
        Windows: in-game
        Linux: logo
    Latest Tested: 2026-10-27
    Url: https://kytyps5.github.io/game/PPSA01317
    """
