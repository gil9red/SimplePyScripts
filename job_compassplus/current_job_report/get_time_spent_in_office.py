#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from dataclasses import dataclass

from utils import session, HOST, NotFoundReport


URL = f"{HOST}/pa-reports-new/report/"


@dataclass
class TimeSpent:
    first_enter: str
    today: str


def get_time_spent_in_office() -> TimeSpent:
    rs = session.get(URL)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    def _find(pattern: str, about: str) -> str:
        if m := re.search(pattern, rs.text, flags=re.IGNORECASE):
            return m.group(1)
        raise Exception(f'Not found {about!r}')

    return TimeSpent(
        first_enter=_find(
            pattern=r"First enter: ([\d+:]+)",
            about="First enter"
        ),
        today=_find(
            pattern=r"Today\s*\(Possible\): ([\d+:]+)",
            about="Today(Possible)"
        ),
    )


if __name__ == "__main__":
    print(get_time_spent_in_office())
    """
    TimeSpent(first_enter='10:53:30', today='07:31:36')
    """
