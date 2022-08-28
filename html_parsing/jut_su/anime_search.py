#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from anime import Anime, send_post, parse_anime_list


def search(text: str) -> list[Anime]:
    rs = send_post(show_search=text)
    return parse_anime_list(rs)


if __name__ == '__main__':
    for anime in search(text='гора'):
        print(anime)
    """
    Anime(url='https://jut.su/shiki/', title='Усопшие')
    Anime(url='https://jut.su/slime-taoshite-300-nen/', title='Убивала слизней 300 лет до максимального уровня')
    Anime(url='https://jut.su/reikenzan/', title='Гора Священного меча')
    Anime(url='https://jut.su/shakunetsu-kabaddi/', title='Пылающий Кабадди')
    """
