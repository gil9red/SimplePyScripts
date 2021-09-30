#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
from pathlib import Path
import shutil

import sys
sys.path.append('..')
sys.path.append('../genre_translate_file')

from db import Dump
from load import load
from common_utils import get_logger
from common import get_current_datetime_str


log = get_logger('generate_games.txt')


DIR = Path(__file__).parent.resolve()
FILE_NAME_GAMES = DIR / 'game_by_genres.json'
FILE_NAME_BACKUP = DIR / 'backup'

FILE_NAME_BACKUP.mkdir(parents=True, exist_ok=True)

# Example: "Action", "Adventure" -> "Action-adventure"
GENRE_COMPRESSION = [
    ("Action", "Adventure", "Action-adventure"),
    ("Action", "RPG", "Action/RPG"),
    ("First-person", "Shooter", "FPS"),
    ("Survival", "Horror", "Survival horror"),
]


def do_genres_compression(genres: list) -> list:
    genres = sorted(set(genres))
    to_remove = set()

    for src_1, src_2, target in GENRE_COMPRESSION:
        if src_1 in genres and src_2 in genres:
            to_remove.add(src_1)
            to_remove.add(src_2)
            genres.append(target)

            log.info(f'Compress genres {src_1!r} and {src_2!r} -> {target!r}')

    for x in to_remove:
        genres.remove(x)

    return sorted(set(genres))


log.info('Start.')

if FILE_NAME_GAMES.exists():
    backup_file_name = str(
        FILE_NAME_BACKUP / f'{get_current_datetime_str()}_{FILE_NAME_GAMES.name}'
    )
    shutil.copy(
        FILE_NAME_GAMES,
        backup_file_name
    )
    log.info(f'Save backup to: {backup_file_name}')
    log.info('')

log.info('Loading cache...')

game_by_genres = load(FILE_NAME_GAMES)
log.info(f'game_by_genres ({len(game_by_genres)})')

new_game_by_genres = Dump.dump()
log.info(f'new_game_by_genres ({len(new_game_by_genres)})')

genre_translate = load()
log.info(f'genre_translate ({len(genre_translate)})')

log.info('Finish loading cache.')
log.info('')

log.info('Search games...')

number = 0

for game, genres in new_game_by_genres.items():
    if game in game_by_genres:
        continue

    log.info(f'Added game {game!r} with genres: {genres}')
    number += 1

    new_genres = []

    for x in genres:
        tr_genres = genre_translate.get(x)
        if not tr_genres:  # null, [], ""
            continue

        if isinstance(tr_genres, str):
            new_genres.append(tr_genres)

        elif isinstance(tr_genres, list):
            new_genres.extend(tr_genres)

        else:
            log.warning(f'Unsupported type genres {tr_genres} from {x!r}')

    new_genres = do_genres_compression(new_genres)

    log.info(f'Successful translate genres: {genres} -> {new_genres}')
    game_by_genres[game] = new_genres

    log.info('')

log.info(f'Finish search games. New games: {number}.')

log.info(f'Saving to {FILE_NAME_GAMES}')

json.dump(
    game_by_genres,
    open(FILE_NAME_GAMES, 'w', encoding='utf-8'),
    ensure_ascii=False,
    indent=4
)

log.info('Finish!')
