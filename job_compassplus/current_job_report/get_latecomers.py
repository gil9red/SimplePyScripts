#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from collections import defaultdict
from datetime import date, datetime
from typing import Callable

from bs4 import BeautifulSoup, Tag
from utils import get_report_context


def get_latecomers(
    dep: str = "dep12",
    period_date: date = None,
    is_latecome: Callable[[datetime], bool] = lambda day: day.hour >= 11,
) -> dict[str, list[datetime]] | None:
    html = get_report_context(
        dep=dep,
        rep="rep2",  # Детальный отчет
        period=period_date.strftime("%Y-%m"),
    )

    root = BeautifulSoup(html, "html.parser")

    person_by_dates: dict[str, list[datetime]] = defaultdict(list)

    report_table = root.select_one("table#report")
    if not report_table:  # Отчет еще не готов
        return None

    dates: list[str | None] = []
    for el in report_table.select("thead > tr:nth-child(2) > th"):
        # NOTE: "17.08" -> (17, 08)
        day, month = map(int, el.get_text(strip=True).split("."))

        d = date(year=period_date.year, month=month, day=day)
        dates.append(d.isoformat() if d.isoweekday() not in (6, 7) else None)

    tr_list = report_table.select("tr:has(td.person)")
    assert tr_list, "Другой формат таблицы. Не нашлось строк с пользователями"

    for tr in tr_list:
        tds: list[Tag] = tr.select("td")
        if len(tds) < 3:
            continue

        # NOTE: Содержит ячейки с временем входа, типа "08:41:18"
        td_person, td_total, td_enter, *td_enter_times = tds
        assert (
            td_enter.get_text(strip=True) == "Вход"
        ), "Другой формат таблицы. Не строка с временем входа"
        assert len(td_enter_times) == len(
            dates
        ), "Другой формат таблицы. Количество столбцов в заголовке и в строке не совпадает"

        # NOTE: Содержит ячейки с временем нахождения, типа "08:41:18" или отсутствия:
        #       "О\n-" - отпуск, "Т\n07:00:00" - временный отпуск и т.п. Время есть, если в офис входили в этот день
        #       (исключение для Т)
        td_time, *td_total_day_times = (
            tr.find_next_sibling("tr").find_next_sibling("tr").select("td")
        )
        assert (
            td_time.get_text(strip=True) == "Время"
        ), "Другой формат таблицы. Не строка с временем нахождения"
        assert len(td_total_day_times) == len(
            dates
        ), "Другой формат таблицы. Количество столбцов в заголовке и в строке не совпадает"

        person: str = td_person.get_text(strip=True)

        # Применительно для текущего пользователя
        if person in person_by_dates:
            continue

        enter_times: list[str | None] = [
            el if re.search(r"\d{2}:\d{2}:\d{2}", el) else None
            for el in map(lambda el: el.get_text(strip=True), td_enter_times)
        ]
        total_day_times: list[str | None] = [
            # Проверка, что в строке есть только цифры и двоеточие
            None if re.sub(r"[\d:\s]", "", el) else el
            for el in map(lambda el: el.get_text(strip=True), td_total_day_times)
        ]

        for date_str, enter_time_str, total_day_time_str in zip(
            dates, enter_times, total_day_times
        ):
            if not date_str or not enter_time_str or not total_day_time_str:
                continue

            day: datetime = datetime.fromisoformat(f"{date_str} {enter_time_str}")
            if is_latecome(day):
                person_by_dates[person].append(day)

    return person_by_dates


if __name__ == "__main__":
    DEP: str = "dep12"

    period_date: date = date.today()
    # NOTE: За конкретную дату
    # period_date: date = date(year=2024, month=9, day=1)
    print(f"Отчет за {period_date:%Y-%m}")

    person_by_dates: dict[str, list[datetime]] | None = get_latecomers(
        dep=DEP, period_date=period_date
    )
    if person_by_dates is None:
        print("Не готов")
    else:
        print(f"Опоздавшие ({len(person_by_dates)}):")
        for person, days in person_by_dates.items():
            print(f"    {person} ({len(days)}):")
            for day in days:
                print(f"        {day}")

            print()

    # NOTE: За период
    # print()
    #
    # for month in [7, 8, 9]:
    #     result = get_latecomers(
    #         dep=DEP, period_date=date(year=2024, month=month, day=1)
    #     )
    #     if not result:
    #         continue
    #
    #     for person, days in result.items():
    #         person_by_dates[person] += days
    #
    # print(f"Опоздавшие ({len(person_by_dates)}):")
    # for person, days in person_by_dates.items():
    #     print(f"    {person} ({len(days)}):")
    #     for day in days:
    #         print(f"        {day}")
    #
    #     print()
