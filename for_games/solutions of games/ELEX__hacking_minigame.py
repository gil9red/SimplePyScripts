#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random


# Этот шаблон допускает любые числа
_ = "*"


def run(
    eval_template: str,
    keys: list[int],
    fixed_values: list[str | int],
    need_values: list[str | int],
):
    while True:
        items = keys.copy()
        fixed_items = fixed_values.copy()
        need_items = need_values.copy()

        # Удаляем дублирующие значения
        for fixed in fixed_items:
            if fixed in items:
                items.remove(fixed)

            if fixed in need_items:
                need_items.remove(fixed)

        random.shuffle(items)
        random.shuffle(need_items)

        free_idx = [i for i, x in enumerate(fixed_items) if x == _]
        random.shuffle(free_idx)

        for i in free_idx:
            # Если есть обязательные значения, то берем из них
            if need_items:
                fixed_items[i] = need_items.pop()
            else:
                fixed_items[i] = items.pop()

        a, b, c, d = fixed_items

        text = (
            eval_template.replace("$1", str(a))
            .replace("$2", str(b))
            .replace("$3", str(c))
            .replace("$4", str(d))
        )

        ok = eval(text)
        if ok:
            print(text)
            break


if __name__ == "__main__":
    run(
        eval_template="$1 == $2 and ($1 > $3 < $4)",
        keys=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        fixed_values=[_, _, _, _],
        need_values=[4],
    )
    # 4 == 4 and (4 > 3 < 8)

    run(
        eval_template="$1 == $2 and ($1 > $3 < $4)",
        keys=[1, 2, 4, 5, 7, 8, 9],
        fixed_values=[_, _, _, _],
        need_values=[4],
    )
    # 4 == 4 and (4 > 2 < 5)

    run(
        eval_template="$1 > $2 > $3 < $4",
        keys=[0, 1, 6, 8],
        fixed_values=[_, _, _, _],
        need_values=[4],
    )
    # 8 > 4 > 1 < 6

    run(
        eval_template="$1 > $2 < $3 > $4",
        keys=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        fixed_values=[_, 1, 8, _],
        need_values=[4],
    )
    # 4 > 1 < 8 > 5
