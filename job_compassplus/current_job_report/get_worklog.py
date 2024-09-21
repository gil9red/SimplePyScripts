#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

from lxml import etree

from utils import get_report_context, NotFoundReport, get_text_children


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

    root = etree.HTML(content)
    items = root.xpath('//table/tbody/tr[contains(@class,"current")]')
    if not items:
        raise NotFoundReport()

    current_user_tr = items[0]
    return Worklog.parse_from(
        (
            # Отработано фактически (чч:мм:сс)
            get_text_children(current_user_tr, 1),

            # Зафиксировано трудозатрат (чч:мм)
            get_text_children(current_user_tr, 2),

            # Процент зафиксированного времени
            get_text_children(current_user_tr, 3),
        )
    )


if __name__ == "__main__":
    print(get_worklog())
    """
    Worklog(actually='103:05:14', logged='66:35', logged_percent=65)
    """
