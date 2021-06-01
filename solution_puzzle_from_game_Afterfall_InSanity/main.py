#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import copy

from dataclasses import dataclass
from typing import List


@dataclass
class Button:
    value: bool
    is_clicked: bool = False


def activate(buttons: List[Button], index: int):
    button = buttons[index]
    if button.is_clicked:
        return

    button.is_clicked = True

    # Немного грубо. Руками указываем индексы кнопок, на которое влияет
    if index == 0:
        ixds = [0, 1]
    elif index == 1:
        ixds = [0, 1, 2]
    else:
        ixds = [1, 2]

    for i in ixds:
        buttons[i].value = not buttons[i].value


def is_win(buttons: List[Button]) -> bool:
    return all(x.value for x in buttons)


def run(init_buttons: List[Button]):
    for start_index in range(len(init_buttons)):
        seq = [start_index]

        buttons = copy.deepcopy(init_buttons)
        activate(buttons, start_index)

        for i in range(len(init_buttons)):
            if i == start_index:
                continue

            seq.append(i)
            activate(buttons, i)

            if is_win(buttons):
                print(seq)
                return


INIT_BUTTONS = [Button(value=False), Button(value=True), Button(value=False)]


if __name__ == '__main__':
    run(INIT_BUTTONS)
