#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from common import session


@dataclass
class Video:
    title: str
    url: str


def get_video_list(url: str) -> dict[str, list[Video]]:
    season_by_video_list = defaultdict(list)

    rs = session.get(url)
    rs.raise_for_status()

    season = ''

    root = BeautifulSoup(rs.content, 'html.parser')

    # Название сезона хранится в <h2>, а сами видео в <a>, причем h2 может и не быть, а сами теги находятся на
    # одном уровне
    for el in root.select_one('#dle-content').find_all(name=['h2', 'a']):
        attr_class = el.get('class', [])

        if el.name == 'h2' and 'the-anime-season' in attr_class:
            season = el.get_text(strip=True)
            continue

        if el.name == 'a' and 'video' in attr_class:
            # Удаление лишнего тега i из <a class="... video ..." href="...html"><i>... </i>1 серия</a>
            el.i.decompose()

            season_by_video_list[season].append(
                Video(
                    title=el.get_text(strip=True),
                    url=urljoin(rs.url, el['href']),
                )
            )

    return season_by_video_list


if __name__ == '__main__':
    import time

    for url in [
        'https://jut.su/zero-kara/',
        'https://jut.su/cowboy-bebop/',
        'https://jut.su/overlord/',
    ]:
        print(url)
        for season, video_list in get_video_list(url).items():
            print(f'"{season}" ({len(video_list)}):')
            for video in video_list:
                print(f'    {video}')
        print()

        time.sleep(1)
    """
    https://jut.su/zero-kara/
    "" (12):
        Video(title='1 серия', url='https://jut.su/zero-kara/episode-1.html')
        Video(title='2 серия', url='https://jut.su/zero-kara/episode-2.html')
        ...
        Video(title='11 серия', url='https://jut.su/zero-kara/episode-11.html')
        Video(title='12 серия', url='https://jut.su/zero-kara/episode-12.html')
    
    https://jut.su/cowboy-bebop/
    "" (26):
        Video(title='1 серия', url='https://jut.su/cowboy-bebop/episode-1.html')
        Video(title='2 серия', url='https://jut.su/cowboy-bebop/episode-2.html')
        ...
        Video(title='25 серия', url='https://jut.su/cowboy-bebop/episode-25.html')
        Video(title='26 серия', url='https://jut.su/cowboy-bebop/episode-26.html')
    "Полнометражные фильмы" (1):
        Video(title='1 фильм', url='https://jut.su/cowboy-bebop/film-1.html')
    
    https://jut.su/overlord/
    "1 сезон" (13):
        Video(title='1 серия', url='https://jut.su/overlord/season-1/episode-1.html')
        Video(title='2 серия', url='https://jut.su/overlord/season-1/episode-2.html')
        ...
        Video(title='12 серия', url='https://jut.su/overlord/season-1/episode-12.html')
        Video(title='13 серия', url='https://jut.su/overlord/season-1/episode-13.html')
    "2 сезон" (13):
        Video(title='1 серия', url='https://jut.su/overlord/season-2/episode-1.html')
        Video(title='2 серия', url='https://jut.su/overlord/season-2/episode-2.html')
        ...
        Video(title='12 серия', url='https://jut.su/overlord/season-2/episode-12.html')
        Video(title='13 серия', url='https://jut.su/overlord/season-2/episode-13.html')
    "3 сезон" (13):
        Video(title='1 серия', url='https://jut.su/overlord/season-3/episode-1.html')
        Video(title='2 серия', url='https://jut.su/overlord/season-3/episode-2.html')
        ...
        Video(title='12 серия', url='https://jut.su/overlord/season-3/episode-12.html')
        Video(title='13 серия', url='https://jut.su/overlord/season-3/episode-13.html')
    "4 сезон" (8):
        Video(title='1 серия', url='https://jut.su/overlord/season-4/episode-1.html')
        Video(title='2 серия', url='https://jut.su/overlord/season-4/episode-2.html')
        ...
        Video(title='7 серия', url='https://jut.su/overlord/season-4/episode-7.html')
        Video(title='8 серия', url='https://jut.su/overlord/season-4/episode-8.html')
    """
