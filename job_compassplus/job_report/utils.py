#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import sys

from datetime import datetime
from collections import defaultdict
from itertools import chain
from pathlib import Path


DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
from current_job_report.get_user_and_deviation_hours import get_report_context

from bs4 import BeautifulSoup

from report_person import ReportPerson


LOGGING_DEBUG = False


if LOGGING_DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)


def get_report_persons_info() -> dict[str, set[ReportPerson]]:
    today = datetime.today().strftime("%Y-%m-%d")
    report_file_name = f"report_{today}.html"

    # Если кэш-файл отчета не существует, загружаем новые данные и сохраняем в кэш-файл
    if not os.path.exists(report_file_name):
        if LOGGING_DEBUG:
            print(f"{report_file_name} not exist")

        context = get_report_context()

        with open(report_file_name, mode="w", encoding="utf-8") as f:
            f.write(context)
    else:
        if LOGGING_DEBUG:
            print(f"{report_file_name} exist")

        with open(report_file_name, encoding="utf-8") as f:
            context = f.read()

    html = BeautifulSoup(context, "lxml")
    report = html.select("#report tbody tr")

    current_dep = None
    report_dict = defaultdict(set)

    for row in report:
        children = list(row.children)
        if len(children) == 1 and children[0].name == "th":
            current_dep = children[0].text.strip()
            continue

        if children[0].has_attr("class") and children[0].attrs["class"][0] == "person":
            person_tags = [children[0].text] + [
                i.text for i in row.nextSibling.select("td")[1:]
            ]
            if len(person_tags) != 8:
                continue

            person = ReportPerson(person_tags)
            report_dict[current_dep].add(person)

    return report_dict


def get_person_info(second_name, first_name=None, middle_name=None, report_dict=None):
    if not report_dict:
        report_dict = get_report_persons_info()

    # Вывести всех сотрудников, отсортировав их по количеству переработанных часов
    for person in list(chain(*report_dict.values())):
        found = person.second_name == second_name

        if first_name is not None:
            found = found and person.first_name == first_name

        if middle_name is not None:
            found = found and person.middle_name == middle_name

        if found:
            return person


if __name__ == "__main__":
    report_dict = get_report_persons_info()
    print(len(report_dict))
    print(sum(map(len, report_dict.values())))
    print()

    for dep, persons in report_dict.items():
        print(f"{dep} ({len(persons)})")
        for p in persons:
            print(f"    {p}")

        print()
