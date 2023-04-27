#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import csv


with open("input.csv") as f:
    dialect = csv.Sniffer().sniff(f.readline())
    # # With delimiters:
    # dialect = csv.Sniffer().sniff(f.readline(), delimiters=[",", ";"])
    f.seek(0)

    csv_reader = csv.reader(f, dialect=dialect)
    for row in csv_reader:
        print(row)
