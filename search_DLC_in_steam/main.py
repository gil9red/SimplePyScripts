#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def is_dlc(game: str) -> bool:
    def steam_search_DLC(name: str) -> list:
        url = "https://store.steampowered.com/search/?category1=21&term=" + name

        game_price_list = []

        while True:
            rs = requests.get(url)
            root = BeautifulSoup(rs.content, "html.parser")
            break

        for div in root.select(".search_result_row"):
            name = div.select_one(".title").text.strip()

            # Ищем тег скидки
            if div.select_one(".search_discount > span"):
                price = div.select_one(".search_price > span > strike").text.strip()
            else:
                price = div.select_one(".search_price").text.strip()

            game_price_list.append((name, price))

        return game_price_list

    # SOURCE: https://github.com/gil9red/price_of_games/blob/9311f9cbc6b9e57d0308436e3dbf3e524f23ef74/app_parser/utils.py
    def smart_comparing_names(name_1: str, name_2: str) -> bool:
        """
        Функция для сравнивания двух названий игр.
        Возвращает True, если совпадают, иначе -- False.

        """

        # Приведение строк к одному регистру
        name_1 = name_1.lower()
        name_2 = name_2.lower()

        def remove_postfix(text: str) -> str:
            for postfix in ("dlc", "expansion"):
                if text.endswith(postfix):
                    return text[: -len(postfix)]
            return text

        # Удаление символов кроме буквенных, цифр и _: "the witcher®3:___ вася! wild hunt" -> "thewitcher3___васяwildhunt"
        def clear_name(name: str) -> str:
            return re.sub(r"\W", "", name)

        name_1 = clear_name(name_1)
        name_1 = remove_postfix(name_1)

        name_2 = clear_name(name_2)
        name_2 = remove_postfix(name_2)

        return name_1 == name_2

    game_dlc_list = steam_search_DLC(game)

    # Сначала пытаемся найти игру по полному совпадению
    for name, price in game_dlc_list:
        if game == name:
            return True

    for name, price in game_dlc_list:
        # Если нашли игру, запоминаем цену и прерываем сравнение с другими найденными играми
        if smart_comparing_names(game, name):
            return True

    return False


# SOURCE: Parser from https://github.com/gil9red/played_games/blob/f23777a1368f9124450bedac036791068d8ca099/mini_played_games_parser.py#L7
def parse_played_games(text: str, silence: bool = False) -> dict:
    """
    Функция для парсинга списка игр.
    """

    FINISHED_GAME = "FINISHED_GAME"
    NOT_FINISHED_GAME = "NOT_FINISHED_GAME"
    FINISHED_WATCHED = "FINISHED_WATCHED"
    NOT_FINISHED_WATCHED = "NOT_FINISHED_WATCHED"

    FLAG_BY_CATEGORY = {
        "  ": FINISHED_GAME,
        "- ": NOT_FINISHED_GAME,
        " -": NOT_FINISHED_GAME,
        " @": FINISHED_WATCHED,
        "@ ": FINISHED_WATCHED,
        "-@": NOT_FINISHED_WATCHED,
        "@-": NOT_FINISHED_WATCHED,
    }

    # Регулярка вытаскивает выражения вида: 1, 2, 3 или 1-3, или римские цифры: III, IV
    PARSE_GAME_NAME_PATTERN = re.compile(
        r"(\d+(, *?\d+)+)|(\d+ *?- *?\d+)|([MDCLXVI]+(, ?[MDCLXVI]+)+)",
        flags=re.IGNORECASE,
    )

    def parse_game_name(game_name: str) -> list:
        """
        Функция принимает название игры и пытается разобрать его, после возвращает список названий.
        У некоторых игр в названии может указываться ее части или диапазон частей, поэтому для правильного
        составления списка игр такие случаи нужно обрабатывать.
        Пример:
            "Resident Evil 4, 5, 6" -> ["Resident Evil 4", "Resident Evil 5", "Resident Evil 6"]
            "Resident Evil 1-3"     -> ["Resident Evil", "Resident Evil 2", "Resident Evil 3"]
            "Resident Evil 4"       -> ["Resident Evil 4"]
        """

        match = PARSE_GAME_NAME_PATTERN.search(game_name)
        if match is None:
            return [game_name]

        seq_str = match.group(0)

        # "Resident Evil 4, 5, 6" -> "Resident Evil"
        # For not valid "Trollface Quest 1-7-8" -> "Trollface Quest"
        index = game_name.index(seq_str)
        base_name = game_name[:index].strip()

        seq_str = seq_str.replace(" ", "")

        if "," in seq_str:
            # '1,2,3' -> ['1', '2', '3']
            seq = seq_str.split(",")

        elif "-" in seq_str:
            seq = seq_str.split("-")

            # ['1', '7'] -> [1, 7]
            seq = list(map(int, seq))

            # [1, 7] -> ['1', '2', '3', '4', '5', '6', '7']
            seq = list(map(str, range(seq[0], seq[1] + 1)))

        else:
            return [game_name]

        # Сразу проверяем номер игры в серии и если она первая, то не добавляем в названии ее номер
        return [base_name if num == "1" else base_name + " " + num for num in seq]

    platforms = dict()
    platform = None

    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            continue

        flag = line[:2]
        if flag not in FLAG_BY_CATEGORY and line.endswith(":"):
            platform_name = line[:-1]

            platform = {
                FINISHED_GAME: [],
                NOT_FINISHED_GAME: [],
                FINISHED_WATCHED: [],
                NOT_FINISHED_WATCHED: [],
            }
            platforms[platform_name] = platform

            continue

        if not platform:
            continue

        category_name = FLAG_BY_CATEGORY.get(flag)
        if not category_name:
            if not silence:
                print('Странный формат строки: "{}"'.format(line))
            continue

        category = platform[category_name]

        game_name = line[2:]
        for game in parse_game_name(game_name):
            if game in category:
                if not silence:
                    print('Предотвращено добавление дубликата игры "{}"'.format(game))
                continue

            category.append(game)

    return platforms


if __name__ == "__main__":
    import time

    with open("gistfile1.txt", encoding="utf-8") as f:
        text = f.read()

    platforms = parse_played_games(text)
    print("Platforms:", len(platforms))

    games = []
    for categories in platforms["PC"].values():
        games += categories

    games = set(games)
    print("Games:", len(games))

    print("DLC:")
    for game in sorted(games):
        if is_dlc(game):
            print("    " + game)

        time.sleep(10)
