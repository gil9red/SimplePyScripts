#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
from typing import Any

import requests

from seconds_to_str import seconds_to_str


URL_BASE = "https://howlongtobeat.com"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"

session = requests.session()
session.headers["User-Agent"] = USER_AGENT


@dataclass
class Game:
    id: int
    title: str
    aliases: list[str]

    duration_main_seconds: int  # Main Story
    duration_main_title: str = field(init=False)

    duration_plus_seconds: int  # Main + Sides
    duration_plus_title: str = field(init=False)

    duration_100_seconds: int  # Completionist
    duration_100_title: str = field(init=False)

    duration_all_seconds: int  # All Styles
    duration_all_title: str = field(init=False)

    release_world: int
    profile_platforms: list[str]

    profile_genres: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.duration_main_title = seconds_to_str(self.duration_main_seconds)
        self.duration_plus_title = seconds_to_str(self.duration_plus_seconds)
        self.duration_100_title = seconds_to_str(self.duration_100_seconds)
        self.duration_all_title = seconds_to_str(self.duration_all_seconds)

    @classmethod
    def parse(cls, data: dict[str, Any]) -> "Game":
        return cls(
            id=data["game_id"],
            title=data["game_name"],
            aliases=data["game_alias"].split(", "),
            duration_main_seconds=data["comp_main"],
            duration_plus_seconds=data["comp_plus"],
            duration_100_seconds=data["comp_100"],
            duration_all_seconds=data["comp_all"],
            release_world=data["release_world"],
            profile_platforms=data["profile_platform"].split(", "),

            # В случаи поиска жанры недоступны в результатах - нужно на страницу игры идти
            profile_genres=data.get("profile_genre", "").split(", "),
        )
