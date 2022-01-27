#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from itertools import cycle


def get_bits_world_seed(world_seed: str) -> str:
    return ''.join(bin(ord(c))[2:][:8].zfill(8) for c in world_seed)


def print_world(world: list[list[int]]):
    print('\n'.join(' '.join(map(str, row)) for row in world))


def fill_world(world: list[list[int]], world_seed: str):
    bits = get_bits_world_seed(world_seed)
    bits = cycle(bits)

    N = len(world)
    for i in range(N * N):
        row, col = divmod(i, N)
        world[row][col] = next(bits)


if __name__ == '__main__':
    assert get_bits_world_seed('1') == '00110001'
    assert get_bits_world_seed('123') == '001100010011001000110011'

    N = 10
    world = [
        [0] * N
        for _ in range(N)
    ]
    print_world(world)

    print()

    world_seed = '123'
    fill_world(world, world_seed)
    print_world(world)
