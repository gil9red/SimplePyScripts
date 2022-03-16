#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import time
from collections import defaultdict

from html_parsing.youtube_com__results_search_query import Playlist, get_raw_video_list


def smart_comparing(game_name: str, playlist_title: str) -> bool:
    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/55b3256c9cfaf338ef0e055c08d8d60720c66c79/html_parsing/get_game_genres/common.py#L31
    def clear_name(name: str) -> str:
        return re.sub(r'\W', '', name)

    clear_game_name = clear_name(game_name).lower()
    clear_playlist_title = clear_name(playlist_title).lower()
    return clear_game_name in clear_playlist_title or clear_playlist_title in clear_game_name


def search_game_playlist(
        game_name: str,
        channel_url: str,
) -> list[tuple[str, str]]:
    playlists = []

    url = f'{channel_url}/search?query={game_name}'
    for obj in get_raw_video_list(url, maximum_items=100):
        playlist_id = obj.get('playlistId')
        if not playlist_id:
            continue

        title = Playlist.get_playlist_title(obj)
        if smart_comparing(game_name, title):
            playlist_url = Playlist.get_url(playlist_id)
            playlists.append((title, playlist_url))

    return playlists


def search_game(
        game_name: str,
        channels: list[tuple[str, str]],
) -> dict[tuple[str, str], list[tuple[str, str]]]:
    channel_by_playlists = defaultdict(list)

    for channel_name, channel_url in channels:
        playlists = search_game_playlist(game_name, channel_url)
        if playlists:
            channel_by_playlists[(channel_name, channel_url)] += playlists

        time.sleep(0.5)

    return channel_by_playlists


if __name__ == '__main__':
    channels = [
        ('Niagara', 'https://www.youtube.com/user/niagaragameplay'),
        ('Two ZZ Games', 'https://www.youtube.com/c/TwoZZGames'),
        ('Лютый Задротер', 'https://www.youtube.com/channel/UCgwwEi1vt9MJMBPV1ohTl-w'),
        ('Velind', 'https://www.youtube.com/c/MrVelind'),
        ('Naritsa', 'https://www.youtube.com/c/Naritsa'),
        ('Disturbing Horror Games', 'https://www.youtube.com/c/DisturbingHorrorGames'),
        ('World of Longplays', 'https://www.youtube.com/recordedamigagames'),
        ('Don Chicko', 'https://www.youtube.com/c/DonChickoPlay'),
        ('Kuplinov ► Play', 'https://www.youtube.com/c/kuplinovplay'),
        ('Сашка Кроп', 'https://www.youtube.com/c/%D0%A1%D0%B0%D1%88%D0%BA%D0%B0%D0%9A%D1%80%D0%BE%D0%BF'),
        ('Hell Play!', 'https://www.youtube.com/c/HellYeahPlay'),
        ('SirOldSchool', 'https://www.youtube.com/c/SirOldSchool'),
        ('OfficialZelel', 'https://www.youtube.com/c/OfficialZelel'),
        ('Копилка с играми', 'https://www.youtube.com/c/%D0%9A%D0%BE%D0%BF%D0%B8%D0%BB%D0%BA%D0%B0%D1%81%D0%B8%D0%B3%D1%80%D0%B0%D0%BC%D0%B8'),
        ('muzzleF', 'https://www.youtube.com/c/muzzleF'),
        ('Белый Ёжик', 'https://www.youtube.com/channel/UCW5G7cZqez0-nUNk1tIR4Lg'),
        ('Sancha777', 'https://www.youtube.com/c/Sancha777'),
        ('Ariona Gamer', 'https://www.youtube.com/c/ArionaGamerChannel'),
        ('Slimt Games', 'https://www.youtube.com/c/SlimtGames'),
        ('Rishin & TimeToPlay', 'https://www.youtube.com/c/Rishin69'),
        ('Никитун', 'https://www.youtube.com/c/NikitunRus'),
        ('Записи Стримов HellYeahPlay', 'https://www.youtube.com/c/HellyeahNetStream'),
        ('Айвори', 'https://www.youtube.com/c/%D0%90%D0%B9%D0%B2%D0%BE%D1%80%D0%B8%D1%82%D0%BE%D0%BF'),
        ('Marmok', 'https://www.youtube.com/c/MrMarmok'),
        ('EugeneSagaz', 'https://www.youtube.com/user/eugenesagaz'),
        ('SAH4R SHOW', 'https://www.youtube.com/c/sah4rshow'),
    ]
    games = [
        'Overwatch', 'Dota 2', 'Apex Legends', 'Enter the Gungeon', 'The Godfather', 'Craft The World',
    ]

    for game_name in games:
        print(f'{game_name!r}:')

        for channel, playlists in search_game(game_name, channels).items():
            channel_title, channel_url = channel
            print(f'    {channel_title!r}: {channel_url}')

            for playlist_title, playlist_url in playlists:
                print(f'        {playlist_title!r}: {playlist_url}')

            print()

        print()

    """
    'Overwatch':
        'Записи Стримов HellYeahPlay': https://www.youtube.com/c/HellyeahNetStream
            'Overwatch': https://www.youtube.com/playlist?list=PLndO6DOY2cLwc4ssIUFxiz9obbWtzmNdJ
    
    
    'Dota 2':
    
    'Apex Legends':
    
    'Enter the Gungeon':
    
    'The Godfather':
        'Don Chicko': https://www.youtube.com/c/DonChickoPlay
            'THE GODFATHER': https://www.youtube.com/playlist?list=PLpvDQIdBrpOwqjSIlErPSPBmcpltadPDH
    
    
    'Craft The World':
    
    """
