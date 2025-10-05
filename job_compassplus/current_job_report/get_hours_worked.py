#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from bs4 import BeautifulSoup, Tag
from utils import (
    NotFoundReport,
    ReportTypeEnum,
    PeriodTypeEnum,
    get_report,
    clear_hours,
)


def get_text_children(el: Tag, idx: int) -> str:
    try:
        return el.find_all(recursive=False)[idx].text.strip()
    except Exception:
        return ""


def get_tr_for_current_user(html: str) -> Tag:
    root = BeautifulSoup(html, "html.parser")

    tbody_el = root.select_one("#report > tbody")
    if not tbody_el:
        tbody_el = root.select_one(".report > tbody")
        if not tbody_el:
            raise NotFoundReport()

    pattern_current_user: re.Pattern = re.compile(".*Текущий пользователь.*")

    th_el = tbody_el.find("th", string=pattern_current_user)
    if not th_el:
        raise NotFoundReport()

    return th_el.parent


def parse_current_user_deviation_hours(html: str) -> tuple[str, str]:
    current_user_tr: Tag = get_tr_for_current_user(html)

    # Получение следующего элемента после текущего, у него получение первого ребенка, у которого вытаскивается текст
    tr_name: Tag = current_user_tr.find_next_sibling()
    name: str = get_text_children(tr_name, idx=0)

    # NOTE: В новом отчете в первой строке указано отклонение
    deviation_hours: str = get_text_children(tr_name, idx=7)
    if not deviation_hours:  # Если старый отчет, то в самом низу
        # Получение следующего элемента после текущего, у него получение последнего
        # ребенка, у которого вытаскивается текст
        # Ищем последнюю строку текущего пользователя -- в ней и находится время работы
        # Ее легко найти -- ее первая ячейка пустая
        deviation_tr = current_user_tr.find_next_sibling()

        # Ищем строку с пустой ячейкой
        while get_text_children(deviation_tr, idx=0):
            deviation_tr = deviation_tr.find_next_sibling()

        deviation_hours: str = get_text_children(deviation_tr, idx=-1)

    return name, clear_hours(deviation_hours)


def get_user_and_deviation_hours() -> tuple[str, str]:
    report: str = get_report(
        report_type=ReportTypeEnum.SUMMARY,
        period_type=PeriodTypeEnum.MONTH,
    )
    return parse_current_user_deviation_hours(report)


def get_quarter_user_and_deviation_hours() -> tuple[str, str]:
    report: str = get_report(
        report_type=ReportTypeEnum.SUMMARY,
        period_type=PeriodTypeEnum.QUARTER,
    )
    return parse_current_user_deviation_hours(report)


if __name__ == "__main__":
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
