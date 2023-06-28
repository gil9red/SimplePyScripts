#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import lxml.html
from html import escape


# SOURCE: https://ru.stackoverflow.com/a/862559/201445
def inner_html(elem):
    # Текст в самом начале внутри тега
    # (не забываем про экранирование!)
    result = [escape(elem.text or "")]

    # Все элементы-потомки
    for child in elem.iterchildren():
        result.append(lxml.html.tostring(child, encoding="unicode"))

    # Текст в конце тега принадлежит последнему элементу-потомку (tail)
    # и добавится автоматически

    # Собираем результат в одну строку
    return "".join(result)


if __name__ == "__main__":
    text = """\
<div id="game_area_description" class="game_area_description">
<strong>Самая популярная игра в Steam</strong>
<br>Ежедневно миллионы игроков по всему миру вступают в битву от лица одного....."""

    node = lxml.html.fragment_fromstring(text)
    print(inner_html(node))
