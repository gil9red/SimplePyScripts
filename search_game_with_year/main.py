#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


# Parser from https://github.com/gil9red/played_games/blob/f23777a1368f9124450bedac036791068d8ca099/mini_played_games_parser.py#L7
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
                print(f'Странный формат строки: "{line}"')
            continue

        category = platform[category_name]

        game_name = line[2:]
        for game in parse_game_name(game_name):
            if game in category:
                if not silence:
                    print(f'Предотвращено добавление дубликата игры "{game}"')
                continue

            category.append(game)

    return platforms


if __name__ == "__main__":
    with open("gistfile1.txt", encoding="utf-8") as f:
        text = f.read()

    platforms = parse_played_games(text)
    print("Platforms:", len(platforms))

    games = list()

    for platform, categories in platforms.items():
        for kind, game_list in categories.items():
            games += game_list

    games = set(games)
    print("Games:", len(games))

    print()
    print("Found:")
    for game in sorted(games):
        match = re.search(r"\s\d{4}\s?", game)
        if match:
            print("    " + game)
