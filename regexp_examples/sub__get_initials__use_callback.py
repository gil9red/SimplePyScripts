#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


text = "Иванов Иван Иванович"

replace_match = lambda x: "{} {}. {}.".format(x[1], x[2][0], x[3][0])
new_text = re.sub(r"(\w+) (\w+) (\w+)", replace_match, text)
print(new_text)  # Иванов И. И.
