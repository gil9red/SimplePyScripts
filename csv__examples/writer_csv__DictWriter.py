#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/csv.html#csv.DictWriter


import csv


with open("names.csv", "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["first_name", "last_name"]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    writer.writerow({"first_name": "Baked", "last_name": "Beans"})
    writer.writerow({"first_name": "Lovely", "last_name": "Spam"})
    writer.writerow({"first_name": "Wonderful", "last_name": "Spam"})
