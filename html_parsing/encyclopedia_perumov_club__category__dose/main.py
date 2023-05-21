#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import re
import time

from bs4 import BeautifulSoup
import requests

import db


def pairwise(t):
    it = iter(t)
    return zip(it, it)


MONKEY_PATCH = {
    "http://encyclopedia.perumov.club/dolina-magov/": lambda text: text.replace(
        "чтQ:", "что:"
    )
}


def parse_dossier(session: requests.Session, url: str) -> list[tuple[str, str]]:
    rs = session.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    p_list = [p.get_text(strip=True) for p in root.select(".content > p")]
    text = "\n".join(p_list)

    if url in MONKEY_PATCH:
        text = MONKEY_PATCH[url](text)

    items = []

    matches = [
        m.span(1)
        for m in re.finditer(r"[AQВО]\s*:(.+?)(?=[AQВО]\s*:)", text, flags=re.DOTALL)
    ]
    if not matches:
        return items

    # From last match to end of text
    last_m = matches[-1]
    matches.append((last_m[1] + 2, len(text)))

    if len(matches) % 2 != 0:
        print(
            f"[#] Warning. In {url} the number of questions does not match the number of answers"
        )

    # Pairs question - answer
    for (q_s, q_e), (a_s, a_e) in pairwise(matches):
        items.append((
            text[q_s: q_e].strip(),
            text[a_s: a_e].strip()
        ))

    return items


if __name__ == "__main__":
    url = "http://encyclopedia.perumov.club/category/dose/"

    session = requests.Session()

    while True:
        print("Page:", url)
        rs = session.get(url)
        root = BeautifulSoup(rs.content, "html.parser")

        for article_el in root.select("article.post"):
            a = article_el.select_one(".header a")

            url_article = a["href"]
            if db.has(url_article):
                continue

            title = a.get_text(strip=True)
            datetime_str = article_el.select_one(".info > time")["datetime"]
            date = DT.datetime.fromisoformat(datetime_str).date()

            items = parse_dossier(session, url_article)
            if not items:
                continue

            db.add(url_article, title, date, items)
            print(f"Added: {title} ({date}, items={len(items)}): {url_article}")

            time.sleep(0.5)

        next_page_el = root.select_one(".pagination > .next[href]")
        if not next_page_el:
            break

        url = next_page_el["href"]

        time.sleep(1)
