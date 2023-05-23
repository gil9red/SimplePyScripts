#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup
import requests


PATTERN_NEXT = re.compile("Следующая →")


def get_comments(url: str, no_quote=False) -> list:
    items = []

    while True:
        rs = requests.get(url)
        root = BeautifulSoup(rs.content, "html.parser")

        # Перебор комментариев
        for comment_text_el in root.select(".comment > div"):
            # Перебор цитат
            for blockquote_el in comment_text_el.select("blockquote"):
                if no_quote:
                    blockquote_el.decompose()
                    continue

                blockquote_el.replace_with(
                    "«" + blockquote_el.get_text(separator="\n", strip=True) + "»"
                )

            for br in comment_text_el.select("br"):
                br.replace_with("\n")

            comment_text = comment_text_el.get_text(separator="\n", strip=True)
            items.append(comment_text)

        a_next = root.find(name="a", text=PATTERN_NEXT)
        if not a_next:
            break

        url = urljoin(rs.url, a_next.get("href"))

    return items


if __name__ == "__main__":
    for url in [
        "https://www.russianfood.com/recipes/recipe.php?rid=107392",
        "https://www.russianfood.com/recipes/recipe.php?rid=121323",
    ]:
        print(url)

        for i, comment_text in enumerate(get_comments(url), 1):
            print(i, repr(comment_text))

        print("\n" + "-" * 100 + "\n")
