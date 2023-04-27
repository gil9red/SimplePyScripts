#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/csv.html#csv.writer


import csv


with open("eggs.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Spam"] * 5 + ["Baked Beans"])
    writer.writerow(["Spam", "Lovely Spam", "Wonderful Spam"])
