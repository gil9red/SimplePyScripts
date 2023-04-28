#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime


def get_age(text: str) -> int:
    date_text = text.split()[0]
    dt = datetime.strptime(date_text, "%d/%m/%Y")
    years_delta = datetime.today() - dt

    return years_delta.days // 365


if __name__ == "__main__":
    text = "31/07/1972 (45 years old)"
    age = get_age(text)
    print(age)  # 45

    text = "18/08/1992"
    age = get_age(text)
    print(age)  # 25
