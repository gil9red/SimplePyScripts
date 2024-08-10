#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import time

from collections import defaultdict

from results_search_query import (
    Playlist,
    Video,
    get_raw_video_list,
)


def smart_comparing(game_name: str, playlist_title: str) -> bool:
    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/55b3256c9cfaf338ef0e055c08d8d60720c66c79/html_parsing/get_game_genres/common.py#L31
    def clear_name(name: str) -> str:
        return re.sub(r"\W", "", name)

    clear_game_name = clear_name(game_name).lower()
    clear_playlist_title = clear_name(playlist_title).lower()
    return (
        clear_game_name in clear_playlist_title
        or clear_playlist_title in clear_game_name
    )


def search_video_and_playlist(
    game_name: str,
    channel_url: str,
) -> list[tuple[str, str]]:
    items = []

    url = f"{channel_url}/search?query={game_name}"
    for obj in get_raw_video_list(url, maximum_items=100):
        if playlist_id := obj.get("playlistId"):
            title = Playlist.get_title(obj)
            if smart_comparing(game_name, title):
                playlist_url = Playlist.get_url(playlist_id)
                items.append((f"[P] {title!r}", playlist_url))
        else:
            title = Video.parse_title(obj)
            if smart_comparing(game_name, title):
                video_url = Video.parse_url(obj)
                items.append((f"[V] {title!r}", video_url))

    return items


def search_game(
    game_name: str,
    channels: list[tuple[str, str]],
) -> dict[tuple[str, str], list[tuple[str, str]]]:
    channel_by_playlists = defaultdict(list)

    for channel_name, channel_url in channels:
        if items := search_video_and_playlist(game_name, channel_url):
            channel_by_playlists[(channel_name, channel_url)] += items

        time.sleep(0.5)

    return channel_by_playlists


if __name__ == "__main__":
    channels = [
        ("Niagara", "https://www.youtube.com/user/niagaragameplay"),
        ("Two ZZ Games", "https://www.youtube.com/c/TwoZZGames"),
        ("Лютый Задротер", "https://www.youtube.com/channel/UCgwwEi1vt9MJMBPV1ohTl-w"),
        ("Velind", "https://www.youtube.com/c/MrVelind"),
        ("Naritsa", "https://www.youtube.com/c/Naritsa"),
        ("Disturbing Horror Games", "https://www.youtube.com/c/DisturbingHorrorGames"),
        ("World of Longplays", "https://www.youtube.com/recordedamigagames"),
        ("Don Chicko", "https://www.youtube.com/c/DonChickoPlay"),
        ("Kuplinov ► Play", "https://www.youtube.com/c/kuplinovplay"),
        (
            "Сашка Кроп",
            "https://www.youtube.com/c/%D0%A1%D0%B0%D1%88%D0%BA%D0%B0%D0%9A%D1%80%D0%BE%D0%BF",
        ),
        ("Hell Play!", "https://www.youtube.com/c/HellYeahPlay"),
        ("SirOldSchool", "https://www.youtube.com/c/SirOldSchool"),
        ("OfficialZelel", "https://www.youtube.com/c/OfficialZelel"),
        (
            "Копилка с играми",
            "https://www.youtube.com/c/%D0%9A%D0%BE%D0%BF%D0%B8%D0%BB%D0%BA%D0%B0%D1%81%D0%B8%D0%B3%D1%80%D0%B0%D0%BC%D0%B8",
        ),
        ("muzzleF", "https://www.youtube.com/c/muzzleF"),
        ("Белый Ёжик", "https://www.youtube.com/channel/UCW5G7cZqez0-nUNk1tIR4Lg"),
        ("Sancha777", "https://www.youtube.com/c/Sancha777"),
        ("Ariona Gamer", "https://www.youtube.com/c/ArionaGamerChannel"),
        ("Slimt Games", "https://www.youtube.com/c/SlimtGames"),
        ("Rishin & TimeToPlay", "https://www.youtube.com/c/Rishin69"),
        ("Никитун", "https://www.youtube.com/c/NikitunRus"),
        ("Записи Стримов HellYeahPlay", "https://www.youtube.com/c/HellyeahNetStream"),
        (
            "Айвори",
            "https://www.youtube.com/c/%D0%90%D0%B9%D0%B2%D0%BE%D1%80%D0%B8%D1%82%D0%BE%D0%BF",
        ),
        ("Marmok", "https://www.youtube.com/c/MrMarmok"),
        ("EugeneSagaz", "https://www.youtube.com/user/eugenesagaz"),
        ("SAH4R SHOW", "https://www.youtube.com/c/sah4rshow"),
    ]
    games = [
        "Overwatch",
        "Dota 2",
        "Apex Legends",
        "Enter the Gungeon",
        "The Godfather",
        "Craft The World",
    ]

    for game_name in games:
        print(f"{game_name!r}:")

        for channel, items in search_game(game_name, channels).items():
            items.sort()

            channel_title, channel_url = channel
            print(f"    {channel_title!r}: {channel_url}")

            for title, url in items:
                print(f"        {title}: {url}")

            print()

        print()

    """
    'Overwatch':
        'Копилка с играми': https://www.youtube.com/c/%D0%9A%D0%BE%D0%BF%D0%B8%D0%BB%D0%BA%D0%B0%D1%81%D0%B8%D0%B3%D1%80%D0%B0%D0%BC%D0%B8
            [V] 'Запись стрима от 13.08.17 по игре OverWatch (Без Наташи)': https://www.youtube.com/watch?v=J2cIv9AT-XQ
    
        'Slimt Games': https://www.youtube.com/c/SlimtGames
            [V] 'Сексизм в видеоиграх? и поза Tracer из игры Overwatch': https://www.youtube.com/watch?v=4Pq62QHiqHQ
    
        'Никитун': https://www.youtube.com/c/NikitunRus
            [V] 'Топ 10 Фактов - Overwatch': https://www.youtube.com/watch?v=3wkJKoHB3h4
    
        'Записи Стримов HellYeahPlay': https://www.youtube.com/c/HellyeahNetStream
            [P] 'Overwatch': https://www.youtube.com/playlist?list=PLndO6DOY2cLwc4ssIUFxiz9obbWtzmNdJ
            [V] 'КТО ПРОЖИВАЕТ НА ДНЕ ОКЕАНА? - Overwatch #3': https://www.youtube.com/watch?v=dv5qDUgrFw0
            [V] 'Лучшие тиммейты - Overwatch #8': https://www.youtube.com/watch?v=vbBlfz1q1Oc
            [V] 'Обучение тактике ДНО - Overwatch #7': https://www.youtube.com/watch?v=AEn_Pf9wOUQ
            [V] 'Попытка победить - Overwatch #9': https://www.youtube.com/watch?v=FmKnka2X9jQ
            [V] 'Рак идет на мид - Overwatch #4': https://www.youtube.com/watch?v=6fhie0_SItU
            [V] 'Ракуем с подписотой - Overwatch #1': https://www.youtube.com/watch?v=1pXXXXrTmSM
            [V] 'ТОЛЬКО ПОБЕДА! - Overwatch #6': https://www.youtube.com/watch?v=zTFTs0mFTb0
            [V] 'Тащу всех на дно - Overwatch #2': https://www.youtube.com/watch?v=sBXQ2Baj-b0
            [V] 'Я самое слабое звено - Overwatch #5': https://www.youtube.com/watch?v=ZL9QuqNhXHs
    
        'Айвори': https://www.youtube.com/c/%D0%90%D0%B9%D0%B2%D0%BE%D1%80%D0%B8%D1%82%D0%BE%D0%BF
            [V] 'OVERWATCH  | ИГРОВЫЕ ФАКТЫ': https://www.youtube.com/watch?v=LuiZ98PtLNM
            [V] 'ТОП 5 ПРОСТЫХ ПЕРСОНАЖЕЙ  OVERWATCH  (ВЫБОР НОВИЧКА)': https://www.youtube.com/watch?v=p3Msb3CqwLs
            [V] 'ТОП 5 САМЫХ БЕСЯЧИХ ПЕРСОНАЖЕЙ OVERWATCH': https://www.youtube.com/watch?v=B6BhYYJI9XU
            [V] 'ТОП 6  ГЕРОЕВ  OVERWATCH  ДЛЯ МЕТКИХ ИГРОКОВ ( НЕТ )': https://www.youtube.com/watch?v=7ZmfYt84Ljk
            [V] 'ТОП 6 ГЕРОЕВ  OVERWATCH НЕОБХОДИМЫХ В КАЖДОЙ ПАТИ': https://www.youtube.com/watch?v=Sg9n1urT2xM
            [V] 'ЭПИЧНЫЙ ОБЗОР НА OVERWATCH': https://www.youtube.com/watch?v=RK0FU6GCjtA
    
        'Marmok': https://www.youtube.com/c/MrMarmok
            [V] '#2 Overwatch - Не зли гориллу': https://www.youtube.com/watch?v=vBc1JpqidR4
    
    
    'Dota 2':
        'Никитун': https://www.youtube.com/c/NikitunRus
            [V] '10 ВЕЩЕЙ, КОТОРЫЕ НЕНАВИДЯТ ИГРОКИ DOTA 2': https://www.youtube.com/watch?v=s7GWzm2r_ZY
    
        'Записи Стримов HellYeahPlay': https://www.youtube.com/c/HellyeahNetStream
            [V] 'ПЛОХОЙ ТИНИ - Dota 2 #2': https://www.youtube.com/watch?v=RSmK6B-UYdc
            [V] 'Раковые Издевательства - Dota 2 #1': https://www.youtube.com/watch?v=yVRv25t52Ds
    
        'SAH4R SHOW': https://www.youtube.com/c/sah4rshow
            [V] 'Sah4R troll #9 CS и Dota2': https://www.youtube.com/watch?v=Yb2Q9NMjL3A
            [V] 'РАКУЕМ В DOTA2 #1 Часть 1/2': https://www.youtube.com/watch?v=uCg5yDk3YgI
            [V] 'РАКУЕМ В DOTA2 #1 Часть 2/2': https://www.youtube.com/watch?v=IqcV9QcmMhI
            [V] 'ШКОЛОСАХАР #61 - CS 1.6, DOTA 2, VRchat': https://www.youtube.com/watch?v=zzkWraUhQLU
    
    
    'Apex Legends':
        'Kuplinov ► Play': https://www.youtube.com/c/kuplinovplay
            [V] 'КУПЛИНОВ И ХЭЛЛОУИН В APEX LEGENDS ► СТРИМ': https://www.youtube.com/watch?v=mNS8K5AxoEY
            [V] 'КУПЛИНОВ ИДЁТ ТАЩИТЬ В APEX LEGENDS ► СТРИМ': https://www.youtube.com/watch?v=fRArg3HNxsQ
    
        'Айвори': https://www.youtube.com/c/%D0%90%D0%B9%D0%B2%D0%BE%D1%80%D0%B8%D1%82%D0%BE%D0%BF
            [V] '6 причин, почему APEX LEGENDS нагнул COD BLACKOUT': https://www.youtube.com/watch?v=4nNu4rAiw70
    
    
    'Enter the Gungeon':
        'Записи Стримов HellYeahPlay': https://www.youtube.com/c/HellyeahNetStream
            [V] 'SubDay №1 - Factorio, Prison Architect, Enter the Gungeon #4': https://www.youtube.com/watch?v=TH8S1zEIecI
            [V] 'Пробуем игру - Enter the Gungeon #1': https://www.youtube.com/watch?v=ktkDK5iQBoM
            [V] 'СТИЛЬ СНАЙПЕРА - Enter the Gungeon #3': https://www.youtube.com/watch?v=W34Yf0M6ICQ
            [V] 'ЭКОНОМНЫЙ ГАННЕР - Enter the Gungeon #2': https://www.youtube.com/watch?v=AA72zpGfXIM
    
    
    'The Godfather':
        'World of Longplays': https://www.youtube.com/recordedamigagames
            [V] 'Amiga 500 Longplay [093] The Godfather': https://www.youtube.com/watch?v=sRO_FggTjc8
            [V] 'Amiga Longplay  The Godfather': https://www.youtube.com/watch?v=4dY5m1QtPBY
    
        'Don Chicko': https://www.youtube.com/c/DonChickoPlay
            [P] 'THE GODFATHER': https://www.youtube.com/playlist?list=PLpvDQIdBrpOwqjSIlErPSPBmcpltadPDH
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 1': https://www.youtube.com/watch?v=_U_5hPxzMSs
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 2': https://www.youtube.com/watch?v=S0lHSn2lZgo
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 3': https://www.youtube.com/watch?v=wr_i15UBzQ4
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 4': https://www.youtube.com/watch?v=HM7LRDCrUx8
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 5': https://www.youtube.com/watch?v=XozoQcq-6zM
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 6': https://www.youtube.com/watch?v=yN-ZDDHgIFw
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 7': https://www.youtube.com/watch?v=9bihljgASPc
            [V] 'THE GODFATHER ► PC ► ПРОХОЖДЕНИЕ ► ЧАСТЬ 8 ► ФИНАЛ': https://www.youtube.com/watch?v=_wPdZUgz9CI
    
        'Hell Play!': https://www.youtube.com/c/HellYeahPlay
            [V] 'БУДУ ГАНГСТЕРОМ! - The Godfather: The Game #1': https://www.youtube.com/watch?v=OF1zzYNJWho
    
    
    'Craft The World':
        'Записи Стримов HellYeahPlay': https://www.youtube.com/c/HellyeahNetStream
            [V] 'Craft The World - Попытка поиграть #2': https://www.youtube.com/watch?v=KtDkBPBMVlc
            [V] 'Craft The World - СТРОИМ БОМБОУБЕЖИЩЕ! #1': https://www.youtube.com/watch?v=V4GFGtACsyE

    """
