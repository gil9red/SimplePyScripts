#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/Marak/zalgo.js/blob/master/zalgo.js


import random

SOUL = {
    "up": [
        '̍', '̎', '̄', '̅',
        '̿', '̑', '̆', '̐',
        '͒', '͗', '͑', '̇',
        '̈', '̊', '͂', '̓',
        '̈', '͊', '͋', '͌',
        '̃', '̂', '̌', '͐',
        '̀', '́', '̋', '̏',
        '̒', '̓', '̔', '̽',
        '̉', 'ͣ', 'ͤ', 'ͥ',
        'ͦ', 'ͧ', 'ͨ', 'ͩ',
        'ͪ', 'ͫ', 'ͬ', 'ͭ',
        'ͮ', 'ͯ', '̾', '͛',
        '͆', '̚'
    ],
    "down": [
        '̖', '̗', '̘', '̙',
        '̜', '̝', '̞', '̟',
        '̠', '̤', '̥', '̦',
        '̩', '̪', '̫', '̬',
        '̭', '̮', '̯', '̰',
        '̱', '̲', '̳', '̹',
        '̺', '̻', '̼', 'ͅ',
        '͇', '͈', '͉', '͍',
        '͎', '͓', '͔', '͕',
        '͖', '͙', '͚', '̣'
    ],
    "mid": [
        '̕', '̛', '̀', '́',
        '͘', '̡', '̢', '̧',
        '̨', '̴', '̵', '̶',
        '͜', '͝', '͞',
        '͟', '͠', '͢', '̸',
        '̷', '͡', ' ҉'
    ]
}
ALL = SOUL['up'] + SOUL['down'] + SOUL['mid']


def _get_random_number(range: int) -> int:
    return random.randrange(range)


def he_comes(text: str, options: dict = None) -> str:
    result = ''

    options = options or dict()
    options["up"] = options.get("up", True)
    options["mid"] = options.get("mid", True)
    options["down"] = options.get("down", True)
    options["size"] = options.get("size", "maxi")

    for l in text:
        if l in ALL:
            continue

        result += l

        counts = {
            "up": 0,
            "down": 0,
            "mid": 0
        }

        if options['size'] == 'mini':
            counts['up'] = _get_random_number(8)
            counts['min'] = _get_random_number(2)
            counts['down'] = _get_random_number(8)

        elif options['size'] == 'maxi':
            counts['up'] = _get_random_number(16) + 3
            counts['min'] = _get_random_number(4) + 1
            counts['down'] = _get_random_number(64) + 3
        else:
            counts['up'] = _get_random_number(8) + 1
            counts['mid'] = _get_random_number(6) / 2
            counts['down'] = _get_random_number(8) + 1

        for index in ["up", "mid", "down"]:
            for _ in range(counts[index]):
                if options[index]:
                    result += random.choice(SOUL[index])

    return result


if __name__ == '__main__':
    for text in ["I'm zalgo", "it's a chain", 'zalgo, he comes']:
        result = he_comes(text)
        print(text)
        print(result)
        print()
