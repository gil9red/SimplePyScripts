#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_game_list_from


url = "https://gematsu.com/exclusives/ps4"
exclusive_games = get_game_list_from(
    url, "fullexclusive", "platformexclusive", "consoleexclusive"
)

print(f"Games ({len(exclusive_games)}):")
for i, game in enumerate(exclusive_games, 1):
    print(f"  {i:3}. {game}")
