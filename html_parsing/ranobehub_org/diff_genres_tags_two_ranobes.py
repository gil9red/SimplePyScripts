#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from get_ranobe_info import get_ranobe_info


def get_common(url_1: str, url_2: str) -> tuple[list[str], list[str]]:
    ranobe_1 = get_ranobe_info(url_1)
    ranobe_2 = get_ranobe_info(url_2)

    genres = []
    for genre in ranobe_1.genres:
        if genre in ranobe_2.genres:
            genres.append(genre)

    tags = []
    for tag in ranobe_1.tags:
        if tag in ranobe_2.tags:
            tags.append(tag)

    return genres, tags


if __name__ == "__main__":
    url_1 = "https://ranobehub.org/ranobe/92-the-legendary-moonlight-sculptor"
    url_2 = "https://ranobehub.org/ranobe/275-everyone-else-is-a-returnee"

    genres, tags = get_common(url_1, url_2)
    print(f"Genres: ({len(genres)}): {genres}")
    # Genres: (7): ['Боевые искусства', 'Комедия', 'Научная фантастика', 'Приключение', 'Сёнэн', 'Фэнтези', 'Экшн']

    print(f"Tags: ({len(tags)}): {tags}")
    # Tags: (23): ['Безжалостный главный герой', 'Бесстыдный главный герой', ..., 'Хорошие отношения с семьей']
