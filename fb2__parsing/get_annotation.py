#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup


def get_annotation(root) -> str:
    annotation_node = root.select_one("description > title-info > annotation")
    if not annotation_node:
        return ""

    return annotation_node.text.strip()


if __name__ == "__main__":
    import glob

    for fb2_file_name in glob.glob("input/*.fb2"):
        print(fb2_file_name)

        with open(fb2_file_name, encoding="utf-8") as f:
            root = BeautifulSoup(f, "html.parser")

        annotation = get_annotation(root)
        print(repr(annotation))
        print(annotation)

        print("\n")
