#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from bs4 import BeautifulSoup, Tag
from utils import (
    NotFoundReport,
    get_report_context,
    get_quarter_report_context,
    clear_hours,
)


def get_text_children(el: Tag, idx: int) -> str:
    try:
        return list(el.children)[idx].text.strip()
    except Exception:
        return ""


def get_tr_for_current_user(html: str) -> Tag:
    root = BeautifulSoup(html, "html.parser")

    tbody_el = root.select_one("#report > tbody")
    if not tbody_el:
        tbody_el = root.select_one(".report > tbody")
        if not tbody_el:
            raise NotFoundReport()

    tr_el = tbody_el.find("tr", text=re.compile(".*Текущий пользователь.*"))
    if not tr_el:
        raise NotFoundReport()

    return tr_el


def parse_current_user_deviation_hours(html: str) -> tuple[str, str]:
    current_user_tr = get_tr_for_current_user(html)

    # Получение следующего элемента после текущего, у него получение первого ребенка, у которого вытаскивается текст
    name = get_text_children(current_user_tr.find_next_sibling(), idx=0)

    # Получение следующего элемента после текущего, у него получение последнего
    # ребенка, у которого вытаскивается текст
    # Ищем последнюю строку текущего пользователя -- в ней и находится время работы
    # Ее легко найти -- ее первая ячейка пустая
    deviation_tr = current_user_tr.find_next_sibling()

    # Ищем строку с пустой ячейкой
    while get_text_children(deviation_tr, idx=0):
        deviation_tr = deviation_tr.find_next_sibling()

    deviation_hours = get_text_children(deviation_tr, idx=-1)
    return name, clear_hours(deviation_hours)


def get_user_and_deviation_hours() -> tuple[str, str]:
    content = get_report_context()
    return parse_current_user_deviation_hours(content)


def get_quarter_user_and_deviation_hours() -> tuple[str, str]:
    content = get_quarter_report_context()
    return parse_current_user_deviation_hours(content)


if __name__ == "__main__":
    """
    Петраш Илья Андреевич
    Переработка 03:27:13

    Петраш Илья Андреевич
    Переработка за квартал 03:27

    Worklog(actually='59:57:13', logged='47:35', logged_percent=79)
    """

    name, deviation_hours = get_user_and_deviation_hours()
    print(name)
    print(
        ("Недоработка" if deviation_hours[0] == "-" else "Переработка")
        + " "
        + deviation_hours
    )
    """
    Петраш Илья Андреевич
    Переработка 04:19:57
    """

    print()

    name, deviation_hours = get_quarter_user_and_deviation_hours()
    print(name)
    print(
        ("Недоработка" if deviation_hours[0] == "-" else "Переработка")
        + " за квартал "
        + deviation_hours
    )
    """
    Петраш Илья Андреевич
    Переработка за квартал 15:09
    """

    print()

    from get_worklog import get_worklog

    print(get_worklog())
    """
    Worklog(actually='103:05:14', logged='66:35', logged_percent=65)
    """
