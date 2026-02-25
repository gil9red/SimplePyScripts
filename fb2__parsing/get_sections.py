#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup


def get_sections_as_dict(root) -> dict[str, dict]:
    # Рекурсивная функция поиска <section>
    def _find_sections(root, root_dict: dict) -> None:
        for section in root.find_all("section", recursive=False):
            title = section.title.text.strip()
            children = dict()

            root_dict[title] = children

            _find_sections(section, children)

    # Первое <body> должно быть с содержанием, описываемое <section>
    body = root.select_one("body")
    section_by_children = dict()

    _find_sections(body, section_by_children)

    return section_by_children


def get_sections_as_list(root) -> list[tuple[str, list]]:
    # Рекурсивная функция поиска <section>
    def _find_sections(root, children_list: list) -> None:
        for section in root.find_all("section", recursive=False):
            title = section.title.text.strip()
            children = []

            children_list.append([title, children])

            _find_sections(section, children)

    # Первое <body> должно быть с содержанием, описываемое <section>
    body = root.select_one("body")
    root_list = []

    _find_sections(body, root_list)

    return root_list


if __name__ == "__main__":
    import glob
    import json

    def _print_sections(root: dict, level=1) -> None:
        for title, children in root.items():
            text = "{}{}".format("    " * (level - 1), title.replace("\n", ". "))
            if children:
                text += ":"

            print(text)
            _print_sections(children, level + 1)

    for fb2_file_name in glob.glob("input/*.fb2"):
        print(fb2_file_name)

        with open(fb2_file_name, encoding="utf-8") as f:
            root = BeautifulSoup(f, "html.parser")

        sections_d = get_sections_as_dict(root)
        print(sections_d)
        print(json.dumps(sections_d, indent=4, ensure_ascii=False))

        sections_l = get_sections_as_list(root)
        print(sections_l)
        print(json.dumps(sections_l, indent=4, ensure_ascii=False))

        print()
        print("Содержание:")
        _print_sections(sections_d, level=2)

        print("\n")
