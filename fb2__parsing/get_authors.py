#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup


def get_authors(root) -> list[str]:
    # Пример тега:
    # <author>
    #     <first-name>Сато</first-name>
    #     <last-name>Цутому</last-name>
    # </author>
    authors_nodes = root.select("description > title-info > author")

    authors = []

    for author in authors_nodes:
        first_name = author.select_one("first-name")
        last_name = author.select_one("last-name")
        middle_name = author.select_one("middle-name")

        name = []

        if first_name:
            name.append(first_name.text)

        if last_name:
            name.append(last_name.text)

        if middle_name:
            name.append(middle_name.text)

        # ['Виталий', 'Зыков'] -> 'Виталий Зыков'
        name = " ".join(name)

        authors.append(name)

    return authors


if __name__ == "__main__":
    import glob

    for fb2_file_name in glob.glob("input/*.fb2"):
        with open(fb2_file_name, encoding="utf-8") as f:
            root = BeautifulSoup(f, "html.parser")

        authors = get_authors(root)
        print(authors)
