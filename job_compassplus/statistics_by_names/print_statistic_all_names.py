#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

from bs4 import BeautifulSoup

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))
from current_job_report.utils import get_report_context


def get_all_names(split_name=False):
    """
    split_name = False: ["<Фамилия> <Имя> <Отчество>", ...]
    split_name = True:  [["<Фамилия>", "<Имя>", "<Отчество>"], ...]

    """

    text = get_report_context()
    root = BeautifulSoup(text, "html.parser")

    # Имена описаны как "<Фамилия> <Имя> <Отчество>"
    items = sorted(
        {" ".join(report.text.split()) for report in root.select("#report .person")}
    )

    if split_name:
        return [x.split(maxsplit=2) for x in items]

    return items


if __name__ == "__main__":
    # Имена описаны как "<Фамилия> <Имя> <Отчество>"
    name_list = get_all_names()

    total = len(name_list)
    print("Total:", total)

    print_line_format = "{:%s}. {}" % len(str(total))

    for i, name in enumerate(name_list, 1):
        print(print_line_format.format(i, name))
