#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"


def parse(url: str) -> tuple[requests.Response, BeautifulSoup]:
    rs = session.get(url)
    return rs, BeautifulSoup(rs.content, "html.parser")
