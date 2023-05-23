#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
import requests


def get_comments(url: str, no_quote=False) -> list:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    items = []

    # Перебор комментариев
    for comment_text_el in root.select(".comment-text"):
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

    return items


if __name__ == "__main__":
    for url in [
        "https://stopgame.ru/show/102770/atom_rpg_review",
        "https://stopgame.ru/show/43787/project_dark_review",
        "https://stopgame.ru/show/82379/dark_souls_iii_videoreview",
    ]:
        print(url)

        for i, comment_text in enumerate(get_comments(url), 1):
            print(i, repr(comment_text))

        print("\n" + "-" * 100 + "\n")
