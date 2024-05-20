#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


import re
from datetime import date

from lxml import etree

from utils import NotFoundReport, get_report_context, get_quarter_report_context, get_year_report_context


def clear_hours(hours: str) -> str:
    return re.sub(r"[^\d:-]", "", hours)


def get_text_children(el: etree._Element, idx) -> str:
    try:
        return el.getchildren()[idx].text.strip()
    except IndexError:
        return ""


def get_tr_for_current_user(html: str) -> etree._Element:
    root = etree.HTML(html)

    xpath_1 = '//table[@id="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]'
    xpath_2 = '//table[@class="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]'

    # Вытаскивание tr, у которого есть вложенный th, имеющий в содержимом текст "Текущий пользователь"
    try:
        items = root.xpath(xpath_1)
        if not items:
            items = root.xpath(xpath_2)

        return items[0]

    except IndexError:
        raise NotFoundReport()


def parse_current_user_deviation_hours(html: str) -> tuple[str, str]:
    current_user_tr = get_tr_for_current_user(html)

    # Получение следующего элемента после текущего, у него получение первого ребенка, у которого вытаскивается текст
    name = get_text_children(current_user_tr.getnext(), idx=0)

    # Получение следующего элемента после текущего, у него получение последнего
    # ребенка, у которого вытаскивается текст
    # Ищем последнюю строку текущего пользователя -- в ней и находится время работы
    # Ее легко найти -- ее первая ячейка пустая
    deviation_tr = current_user_tr.getnext()

    # Ищем строку с пустой ячейкой
    while get_text_children(deviation_tr, idx=0):
        deviation_tr = deviation_tr.getnext()

    deviation_hours = get_text_children(deviation_tr, idx=-1)
    return name, clear_hours(deviation_hours)


def parse_user_deviation_hours(html: str, user_name: str = "Петраш") -> tuple[str, str]:
    root = etree.HTML(html)

    XPATH_1 = f'//table[@id="report"]/tbody/tr[td[contains(text(),"{user_name}")]]'
    XPATH_2 = f'//table[@class="report"]/tbody/tr[td[contains(text(),"{user_name}")]]'

    # Вытаскивание tr, у которого есть вложенный th, имеющий в содержимом текст "Текущий пользователь"
    try:
        items = root.xpath(XPATH_1)
        if not items:
            items = root.xpath(XPATH_2)

        current_user_tr = items[0]

    except IndexError:
        raise NotFoundReport()

    # Получение текста текущего элемента
    name = get_text_children(current_user_tr, idx=0)

    # Получение следующего элемента после текущего, у него получение последнего
    # ребенка, у которого вытаскивается текст
    # Ищем последнюю строку текущего пользователя -- в ней и находится время работы
    # Ее легко найти -- ее первая ячейка пустая
    deviation_tr = current_user_tr.getnext()

    # Ищем строку с пустой ячейкой
    while get_text_children(deviation_tr, idx=0):
        deviation_tr = deviation_tr.getnext()

    deviation_hours = get_text_children(deviation_tr, idx=-1)
    return name, clear_hours(deviation_hours)


def get_current_user_for_year_vacations() -> tuple[str, list[date]]:
    html = get_year_report_context()
    current_user_tr = get_tr_for_current_user(html).getnext()

    # Получение текста текущего элемента
    name = get_text_children(current_user_tr, idx=0)

    vacations = []

    # Ищем строку с пустой ячейкой
    tr = current_user_tr
    while True:
        try:
            key = get_text_children(tr, idx=0)
            if not key:
                break

            if key.lower() != "отпуск":
                continue

            value = get_text_children(tr, idx=1)
            if not value:
                continue

            vacations.append(
                date.fromisoformat(value)
            )

        finally:
            tr = tr.getnext()

    return name, vacations


def get_human_list_of_vacations(vacations: list[date]) -> list[str]:
    def get_date_range(date1: date, date2: date, fmt: str = "%d.%m") -> str:
        return f"{date1.strftime(fmt)}-{date2.strftime(fmt)}"

    items = []
    if not vacations:
        return items

    prev_date = start_date = vacations[0]
    for d in vacations[1:]:
        if (d - prev_date).days > 1:
            items.append(get_date_range(start_date, prev_date))
            start_date = d

        prev_date = d

    items.append(get_date_range(start_date, prev_date))
    return items


def get_user_and_deviation_hours() -> tuple[str, str]:
    content = get_report_context()
    return parse_current_user_deviation_hours(content)


def get_quarter_user_and_deviation_hours() -> tuple[str, str]:
    content = get_quarter_report_context()
    return parse_user_deviation_hours(content)


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

    name, vacations = get_current_user_for_year_vacations()
    print(name)
    print(f"Использовано отпускных дней: {len(vacations)}")
    if vacations:
        print(", ".join(get_human_list_of_vacations(vacations)))
    """
    Петраш Илья Андреевич
    Использовано отпускных дней: 14
    17.01-18.01, 29.02-01.03, 18.03-22.03, 25.03-29.03
    """
