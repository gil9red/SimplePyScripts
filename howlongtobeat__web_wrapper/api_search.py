#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import unicodedata

from typing import Any

# NOTE: https://playwright.dev/python/docs/library#pip
#   pip install playwright==1.50.0
#   playwright install webkit
from playwright.sync_api import sync_playwright, Response


def _is_found_game(game1: str, game2: str) -> bool:
    # SOURCE: https://github.com/gil9red/price_of_games/blob/805f19528c3bcc0999669452c3652698fed22bcd/app_parser/utils.py#L219-L224
    def strip_accents(s: str) -> str:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )

    def _process_name(name: str) -> str:
        name = strip_accents(name)
        return re.sub(r"\W", "", name).lower()

    return _process_name(game1) == _process_name(game2)


def get_api_search_raw(game: str) -> dict[str, Any]:
    with sync_playwright() as p:
        browser = p.webkit.launch()

        page = browser.new_page()
        page.set_default_timeout(90_000)

        page.goto(f"https://howlongtobeat.com/?q={game}", wait_until="commit")

        def is_api_search(rs: Response) -> bool:
            url: str = rs.url.lower()
            return (
                "/api/" in url
                and rs.status == 200
                and ("SEARCHTERMS" in str(rs.request.post_data).upper())
            )

        with page.expect_response(is_api_search) as response_info:
            return response_info.value.json()


def search_game(game: str) -> dict[str, Any] | None:
    game: str = re.sub("[©®™–]", "", game).replace("`", "'")

    result: dict[str, Any] = get_api_search_raw(game)
    for obj in result["data"]:
        if (
            _is_found_game(game, obj["game_name"])
            # Поиск среди псевдонимов
            or obj["game_alias"] == game
            or any(_is_found_game(game, name) for name in obj["game_alias"].split(", "))
        ):
            return obj

    return


if __name__ == "__main__":
    game = "Warhammer 40,000: Space Marine 2"
    result = search_game(game)
    print(game, result)
    assert "Warhammer 40,000: Space Marine II" == result["game_name"]

    game = "Half-Life 2"
    result = search_game(game)
    print(game, result)
    assert game == result["game_name"]

    game = "Marc Eckō's Getting Up: Contents Under Pressure"
    result = search_game(game)
    print(game, result)
    assert "Marc Ecko's Getting Up: Contents Under Pressure" == result["game_name"]

    game = "Nightmares from the Deep 2: The Siren`s Call"
    result = search_game(game)
    print(game, result)
    assert "Nightmares from the Deep 2: The Siren's Call" == result["game_name"]

    print()

    game = search_game("Half-Life")
    print(game)
    assert game

    game = search_game("Final Fantasy IX")
    print(game)
    assert game

    game = search_game("Final Fantasy 9")
    print(game)
    assert game

    game = search_game("Final Fantasy VII")
    print(game)
    assert game

    # from multiprocessing.dummy import Pool as ThreadPool
    #
    # with ThreadPool() as p:
    #     result = p.map(
    #         search_game,
    #         [
    #             "dfsdfsdfsdfsdfsdfsdfdsf",
    #             "Half-Life 2",
    #             "Half-Life",
    #             "Final Fantasy",
    #             "Final Fantasy IX",
    #             "Final Fantasy 9",
    #             "Final Fantasy VII",
    #         ],
    #     )
    #     print(len(result))
    #     for obj in result:
    #         print(obj)
