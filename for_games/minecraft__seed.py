#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://minecraft-ru.gamepedia.com/Зерно
# Последовательность в поле ввода преобразуется с помощью Java-функции String.hashCode().
# Например, строка «abc» конвертируется в числовое значение 97×31² + 98×31 + 99 = 96354.


def get_value_seed_v1(seed: str) -> int:
    return sum(map(lambda x: x[1] * (31 ** x[0]), enumerate(map(ord, reversed(seed)))))


def get_value_seed_v2(seed: str) -> int:
    value = 0

    for i in range(len(seed)):
        j = (len(seed) - 1) - i

        value += ord(seed[i]) * (31**j)

    return value


def get_value_seed_v3(seed: str) -> int:
    return sum(ord(seed[i]) * (31 ** ((len(seed) - 1) - i)) for i in range(len(seed)))


if __name__ == "__main__":
    # print(97 * 31 ** 2 + 98 * 31 + 99)

    print(get_value_seed_v1("abc"))
    print(get_value_seed_v2("abc"))
    print(get_value_seed_v3("abc"))

    assert get_value_seed_v1("abc") == 96354
    assert get_value_seed_v2("abc") == 96354
    assert get_value_seed_v3("abc") == 96354
