#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def smart_comparing_names(name_1, name_2):
    """
    Функция для сравнивания двух названий игр.
    Возвращает True, если совпадают, иначе -- False.

    """

    # Приведение строк к одному регистру
    name_1 = name_1.lower()
    name_2 = name_2.lower()

    def remove_postfix(text: str, postfix='(dlc)') -> str:
        if text.endswith(postfix):
            text = text[:-len(postfix)]

        return text

    # Удаление символов кроме буквенных, цифр и _: "the witcher®3:___ вася! wild hunt" -> "thewitcher3___васяwildhunt"
    def clear_name(name: str) -> str:
        import re
        return re.sub(r'\W|the', '', name)

    name_1 = remove_postfix(name_1)
    name_2 = remove_postfix(name_2)

    return clear_name(name_1) == clear_name(name_2)


TEST_GAMES = [
    'Hellgate: London',
    'The Incredible Adventures of Van Helsing',
    'Dark Souls: Prepare to Die Edition',
    'Twin Sector',
    'Call of Cthulhu: Dark Corners of the Earth',
]


def _common_test(search_game_genres, get_game_genres, sleep=1, max_number=len(TEST_GAMES)):
    import time

    for name in TEST_GAMES[:max_number]:
        items = search_game_genres(name)
        print(f'Search {name!r}...')
        print(f'  Result ({len(items)}):')
        for game, genres in items:
            print(f'    {game!r}: {genres}')
        print()
        print(f'Genres: {get_game_genres(name)}')

        print('\n' + '-' * 20 + '\n')

        time.sleep(sleep)
