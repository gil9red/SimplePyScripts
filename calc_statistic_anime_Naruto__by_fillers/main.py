#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import re

import requests


def get_html_by_url__from_cache(url, cache_dir="cache"):
    os.makedirs(cache_dir, exist_ok=True)

    file_name = os.path.basename(url)
    file_name = re.sub(r"\W", "_", file_name)

    file_name = cache_dir + "/" + file_name + ".html"

    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return f.read()

    with open(file_name, "wb") as f:
        rs = requests.get(url)
        f.write(rs.content)

        return rs.content


def get_ep_chapters_s1():
    def get_urls_of_season():
        return [
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_1—3)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_4—6)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_7—9)",
        ]

    from bs4 import BeautifulSoup

    ep_chapters = []

    for url in get_urls_of_season():
        html_content = get_html_by_url__from_cache(url)

        root = BeautifulSoup(html_content, "html.parser")

        for td in root.select("td"):
            if td.has_attr("id") and td["id"].startswith("ep"):
                episode = td.text.strip()
                manga_chapters = td.next_sibling.next_sibling.text.strip()

                ep_chapters.append((episode, manga_chapters))

    return ep_chapters


def get_ep_chapters_s2():
    def get_urls_of_season():
        return [
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_1—4)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_5—8)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_9—12)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_13—16)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_17—20)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_21—24)",
            "https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_25—28)",
        ]

    from bs4 import BeautifulSoup

    ep_chapters = []

    for url in get_urls_of_season():
        html_content = get_html_by_url__from_cache(url)

        root = BeautifulSoup(html_content, "html.parser")

        for td in root.select("td"):
            if td.has_attr("id") and td["id"].startswith("ep"):
                episode = td.text.strip()
                manga_chapters = td.next_sibling.next_sibling.next_sibling.text.strip()

                ep_chapters.append((episode, manga_chapters))

    return ep_chapters


def calc_statistic(ep_chapters: list) -> (int, int, int, int):
    number_all_ep = len(ep_chapters)
    number_filler_ep = len([x for x in ep_chapters if "Нет (филлер)" in x[1]])
    number_manga_ep = number_all_ep - number_filler_ep
    precent_filler = number_filler_ep / number_all_ep * 100

    return number_all_ep, number_manga_ep, number_filler_ep, precent_filler


if __name__ == "__main__":
    ep_chapters_s1 = get_ep_chapters_s1()
    number_all_ep_s1, _, number_filler_ep_s1, precent_filler_s1 = calc_statistic(
        ep_chapters_s1
    )
    print(
        f"Season 1.\n"
        f"    Total: {number_all_ep_s1}, fillers: {number_filler_ep_s1} ({precent_filler_s1:.1f}%)\n"
    )

    ep_chapters_s2 = get_ep_chapters_s2()
    number_all_ep_s2, _, number_filler_ep_s2, precent_filler_s2 = calc_statistic(
        ep_chapters_s2
    )
    print(
        f"Season 2.\n"
        f"    Total: {number_all_ep_s2}, fillers: {number_filler_ep_s2} ({precent_filler_s2:.1f}%)\n"
    )

    ep_chapters_s1_2 = ep_chapters_s1 + ep_chapters_s2
    number_all_ep_s1_2, _, number_filler_ep_s1_2, precent_filler_s1_2 = calc_statistic(
        ep_chapters_s1_2
    )
    print(
        f"Season 1+2.\n"
        f"    Total: {number_all_ep_s1_2}, fillers: {number_filler_ep_s1_2} ({precent_filler_s1_2:.1f}%)\n"
    )

# Season 1.
#     Total: 220, fillers: 93 (42.3%)
#
# Season 2.
#     Total: 500, fillers: 187 (37.4%)
#
# Season 1+2.
#     Total: 720, fillers: 280 (38.9%)
