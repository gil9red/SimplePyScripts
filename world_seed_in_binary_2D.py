#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random
import string

from itertools import cycle


def get_random_seed(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_bits_seed(seed: str) -> str:
    return ''.join(bin(ord(c))[2:][:8].zfill(8) for c in seed)


def create_world(rows: int, cols: int) -> list[list[int]]:
    return [
        [0] * cols
        for _ in range(rows)
    ]


def print_world(world: list[list[int]]):
    print('\n'.join(' '.join(map(str, row)) for row in world))


def fill_world(world: list[list[int]], seed: str):
    bits = get_bits_seed(seed)
    bits = cycle(bits)

    for row in range(len(world)):
        for col in range(len(world[0])):
            world[row][col] = next(bits)


if __name__ == '__main__':
    for i in range(8, 64+1):
        assert len(get_random_seed(length=i)) == i

    print('Random seed:', get_random_seed())
    print()

    assert get_bits_seed('1') == '00110001'
    assert get_bits_seed('123') == '001100010011001000110011'

    world = create_world(rows=5, cols=10)
    print_world(world)

    print()

    fill_world(world, seed='123')
    print_world(world)
