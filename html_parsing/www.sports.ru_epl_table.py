#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup


def parse(html):
    soup = BeautifulSoup(html, "lxml")

    teams = []

    for row in soup.select("tbody > tr"):
        cols = row.select("td")

        teams.append({
            "Место": cols[0].text,
            "Команда": [name.text for name in row.select("a[class=name]")],
            "Матчи": cols[2].text,
        })

    return teams


if __name__ == "__main__":
    url = "https://www.sports.ru/epl/table/"

    import urllib.request

    with urllib.request.urlopen(url) as rs:
        html = rs.read()

    teams = parse(html)

    for team in teams:
        print(team)
