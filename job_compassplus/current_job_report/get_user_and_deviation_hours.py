#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


from lxml import etree

from utils import (
    NotFoundReport,
    get_report_context,
    get_quarter_report_context,
    clear_hours,
)


def get_text_children(el: etree._Element, idx: int) -> str:
    try:
        return el.getchildren()[idx].text.strip()
    except IndexError:
        return ""


def get_tr_for_current_user(html: str) -> etree._Element:
    root = etree.HTML(html)

    xpath_1 = (
        '//table[@id="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]'
    )
    xpath_2 = (
        '//table[@class="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]'
    )

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


def get_user_and_deviation_hours() -> tuple[str, str]:
    content = get_report_context()
    return parse_current_user_deviation_hours(content)


def get_quarter_user_and_deviation_hours() -> tuple[str, str]:
    content = get_quarter_report_context()
    return parse_current_user_deviation_hours(content)


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
