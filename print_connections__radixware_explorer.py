#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from bs4 import BeautifulSoup

# pip install tabulate
from tabulate import tabulate


FILE_NAME = r"%APPDATA%\radixware.org\explorer\connections.xml"
ABS_FILE_NAME = os.path.expandvars(FILE_NAME)


with open(ABS_FILE_NAME, "rb") as f:
    root = BeautifulSoup(f.read(), "html.parser")


def get_tag_text(tag):
    return "<NULL>" if tag is None else tag.text


headers = [
    "NAME",
    "ID",
    "COMMENT",
    "USERNAME",
    "STATIONNAME",
    "INITIALADDRESS",
    "LANGUAGE",
    "COUNTRY",
    "EXPLORERROOTID",
    "TRACELEVEL",
]
rows = []

for connection in root.select("connection"):
    rows.append(
        [
            connection["name"],
            connection["id"],
            get_tag_text(connection.comment),
            get_tag_text(connection.username),
            get_tag_text(connection.stationname),
            get_tag_text(connection.initialaddress),
            get_tag_text(connection.language),
            get_tag_text(connection.country),
            get_tag_text(connection.explorerrootid),
            get_tag_text(connection.tracelevel),
        ]
    )


print(tabulate(rows, headers=headers, tablefmt="grid"))
