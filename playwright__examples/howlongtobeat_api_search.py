#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from typing import Any

# NOTE: https://playwright.dev/python/docs/library#pip
#   pip install playwright
#   playwright install webkit
from playwright.sync_api import sync_playwright, Response


def get_api_search_raw(game: str) -> dict[str, Any]:
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()

        page.goto(f"https://howlongtobeat.com/?q={game}", wait_until="commit")

        def is_api_search(rs: Response) -> bool:
            url: str = rs.url.lower()

            return ("/api/search" in url or "/api/find" in url) and rs.status == 200

        with page.expect_response(is_api_search) as response_info:
            return response_info.value.json()


def search_game(game: str) -> dict[str, Any] | None:
    game = re.sub("[©®–]", "", game)

    def _is_found_game(game1: str, game2: str):
        def _process_name(name: str):
            return re.sub(r"\W", "", name).lower()

        return _process_name(game1) == _process_name(game2)

    result: dict[str, Any] = get_api_search_raw(game)
    for obj in result["data"]:
        if (
            _is_found_game(game, obj["game_name"])
            # Поиск среди псевдонимов
            or any(_is_found_game(game, name) for name in obj["game_alias"].split(","))
        ):
            return obj

    return


if __name__ == "__main__":
    game = "Half-Life 2"
    result = search_game(game)
    print(game, result)
    assert game == result["game_name"]

    # print(search_game("Half-Life 2"))
    # print(search_game("Half-Life"))
    # print(search_game("Final Fantasy IX"))
    # print(search_game("Final Fantasy 9"))
    # print(search_game("Final Fantasy VII"))

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
