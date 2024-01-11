#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import copy


def activate(cylinders: list[bool], index: int):
    left_index = (index - 1) % len(cylinders)
    right_index = (index + 1) % len(cylinders)

    cylinders[left_index] = not cylinders[left_index]
    cylinders[index] = not cylinders[index]
    cylinders[right_index] = not cylinders[right_index]


def is_win(cylinders: list[bool]) -> bool:
    return all(cylinders)


def run(init_cylinders: list[bool]):
    for start_index in range(len(init_cylinders)):
        seq = [start_index]

        cylinders = copy.deepcopy(init_cylinders)
        activate(cylinders, start_index)

        for i in range(len(cylinders)):
            if i == start_index:
                continue

            seq.append(i)
            activate(cylinders, i)

            if is_win(cylinders):
                print(seq)
                return


CYLINDERS: list[bool] = [False] * 8


if __name__ == "__main__":
    run(CYLINDERS)
    # [0, 1, 2, 3, 4, 5, 6, 7]
