#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from extract_all_games import cache


print(f'Всего игр: {len(cache)}')
print()
# Всего игр: 11301

games = []
for game, time_obj in cache.items():
    seconds = time_obj['seconds']
    if not seconds or game.upper().endswith('DLC'):
        continue

    games.append((game, time_obj['text'], seconds))

# Сортировка по возрастанию времени прохождения
games.sort(key=lambda x: x[2])

n = 100
print(f'Первые {n} игр с минимум времени прохождения:')
for i, (game, time_text, _) in enumerate(games[:n], 1):
    print(f'{i:3}. {game!r}: {time_text}')
"""
Первые 100 игр с минимум времени прохождения:
  1. 'Mitoza': 1 мин.
  2. 'Lost in Space (2018)': 1 мин.
  3. 'Run Jesus Run a.k.a. The 10 Second Gospel': 1 мин.
  4. 'First Job': 2 мин.
  5. 'Sakuya Izayoi Gives You Advice And Dabs': 2 мин.
...
 96. 'Star Gladiator': 11 мин.
 97. 'Flightless (2017)': 11 мин.
 98. 'Kimulator: Fight for your destiny': 11 мин.
 99. 'UBERMOSH Vol.3': 11 мин.
100. 'A Game About': 12 мин.
"""
