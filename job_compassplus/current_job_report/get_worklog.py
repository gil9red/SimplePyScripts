#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from bs4 import BeautifulSoup
from utils import get_report_context, NotFoundReport


@dataclass
class Worklog:
    actually: str  # Отработано фактически (чч:мм:сс)
    logged: str  # Зафиксировано трудозатрат (чч:мм)
    logged_percent: int  # Процент зафиксированного времени

    @classmethod
    def parse_from(cls, data: tuple[str, str, str]) -> "Worklog":
        return cls(
            actually=data[0],
            logged=data[1],
            logged_percent=int(data[2].replace("%", "")),
        )


def get_worklog() -> Worklog:
    content = get_report_context(rep="worklog")

    root = BeautifulSoup(content, "html.parser")
    current_user_tr = root.select_one("table > tbody > tr.current")
    if not current_user_tr:
        raise NotFoundReport()

    td_list = current_user_tr.select("td")
    return Worklog.parse_from(
        (
            # Отработано фактически (чч:мм:сс)
            td_list[1].get_text(strip=True),

            # Зафиксировано трудозатрат (чч:мм)
            td_list[2].get_text(strip=True),

            # Процент зафиксированного времени
            td_list[3].get_text(strip=True),
        )
    )


if __name__ == "__main__":
    print(get_worklog())
    """
    Worklog(actually='103:05:14', logged='66:35', logged_percent=65)
    """
