#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
from pathlib import Path

from main import find


DIR = Path(os.path.expanduser(r'~\Desktop\Пройти'))
game_names = [p.stem for p in DIR.glob('*.lnk')]

items = []
for game in game_names:
    data = find(game)
    if data:
        items.append((game, data['Основной сюжет']))

    time.sleep(1)

# Сортировка по возрастанию времени прохождения
items.sort(key=lambda x: x[1].seconds)

print('Первые 10 игр с минимум времени прохождения:')
for i, (game, time) in enumerate(items[:10], 1):
    print(f'{i:2}. {game!r}: {time.text}')
"""
Первые 10 игр с минимум времени прохождения:
 1. 'FOTONICA': 2 ч. 11 мин.
 2. 'The Wild Eight': 4 ч.
 3. 'Sonic Forces': 4 ч. 12 мин.
 4. 'Halo - Spartan Assault': 4 ч. 17 мин.
 5. 'NecroVision Lost Company': 4 ч. 52 мин.
 6. 'Niko - Through the Dream': 5 ч. 21 мин.
 7. 'FEZ': 5 ч. 52 мин.
 8. 'Lucius': 6 ч. 13 мин.
 9. 'Flashback': 6 ч. 14 мин.
10. 'True Crime - New York City': 7 ч.
"""
