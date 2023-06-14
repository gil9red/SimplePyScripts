#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def template(template_text, map_values):
    for match in re.findall("<(.+?)>", text):
        if match in map_values:
            template_text = template_text.replace("<" + match + ">", map_values[match])

    return template_text


if __name__ == "__main__":
    text = "Я купил тебе, <имя>, <любая фигня>!"

    new_text = template(text, {"имя": "милая", "любая фигня": "вишню"})
    print(new_text)

    new_text = template(
        text, {"имя": "Иван Петрович", "любая фигня": "большой андронный коллайдер"}
    )
    print(new_text)
