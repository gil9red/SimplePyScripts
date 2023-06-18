#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib
import random
import string

from itertools import cycle


def get_random_seed(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_bits_seed(seed: str) -> str:
    seed = bytes(seed, encoding="utf-8")
    return "".join(bin(c)[2:][:8].zfill(8) for c in hashlib.sha256(seed).digest())


def create_world(rows: int, cols: int) -> list[list[int]]:
    return [[0] * cols for _ in range(rows)]


def print_world(world: list[list[int]]):
    print("\n".join(" ".join(map(str, row)) for row in world))


def fill_world(world: list[list[int]], seed: str):
    bits = get_bits_seed(seed)
    bits = cycle(bits)

    for row in range(len(world)):
        for col in range(len(world[0])):
            world[row][col] = int(next(bits))


if __name__ == "__main__":
    for i in range(8, 64 + 1):
        assert len(get_random_seed(length=i)) == i

    print("Random seed:", get_random_seed())
    print()

    assert (
        get_bits_seed("1")
        == "0110101110000110101100100111001111111111001101001111110011100001100111010110101110000000010011101111111101011010001111110101011101000111101011011010010011101010101000100010111100011101010010011100000000011110010100101101110110110111100001110101101101001011"
    )
    assert (
        get_bits_seed("123")
        == "1010011001100101101001000101100100100000010000100010111110011101010000010111111001001000011001111110111111011100010011111011100010100000010010100001111100111111111111110001111110100000011111101001100110001110100001101111011111110111101000100111101011100011"
    )

    world = create_world(rows=5, cols=10)
    print_world(world)

    print()

    fill_world(world, seed="123")
    print_world(world)
