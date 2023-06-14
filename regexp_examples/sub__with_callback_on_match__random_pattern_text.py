#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import re


def random_text(text: str) -> str:
    def _on_sub_process(match) -> str:
        # "Дима,Вася,Игорь" -> ["Дима", "Вася", "Игорь"]
        variants = match.group(1).split(",")
        return random.choice(variants)

    # В регулярке выполняется замена выражений внутри круглых скобок
    return re.sub(r"\((.+?)\)", _on_sub_process, text)


text = "Привет, (Дима,Вася,Игорь)! (Как дела?,Как настроение?,Как жизнь?) Пойдешь (завтра,сегодня,на следующей неделе) на тренировку?"
new_text = random_text(text)
print(new_text)  # Привет, Игорь! Как настроение? Пойдешь сегодня на тренировку?

new_text = random_text(text)
print(new_text)  # Привет, Дима! Как жизнь? Пойдешь сегодня на тренировку?
