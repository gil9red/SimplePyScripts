#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re
import time

from dataclasses import dataclass
from datetime import datetime, date
from typing import Any, Self

from playwright.sync_api import sync_playwright


HOST: str = "https://com-x.life"
URL: str = f"{HOST}/2789-berserk-read-online.html#chapters"


@dataclass
class Chapter:
    title: str
    url: str
    pages: int
    date: date

    @classmethod
    def from_dict(cls, chapter_id: int, d: dict[str, Any]) -> Self:
        return cls(
            title=d["title"],
            url=f"{HOST}/reader/{chapter_id}/{d['id']}",
            pages=d["pages"],
            date=datetime.strptime(d["date"], "%d.%m.%Y").date(),
        )


def get_chapters() -> list[Chapter]:
    chapters: list[Chapter] = []

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()

        page.goto(URL)

        for _ in range(10):
            time.sleep(1)

            text: str = page.content()

            m = re.search(r"window.__DATA__\s*=\s*(\{.+?\});", text)
            if not m:
                continue

            data: dict[str, Any] = json.loads(m.group(1))
            chapter_id: int = data["news_id"]
            chapters = [
                Chapter.from_dict(chapter_id, chapter)
                for chapter in data["chapters"]
            ]
            break

    if not chapters:
        raise Exception("Не удалось найти главы!")

    return chapters


if __name__ == "__main__":
    chapters = get_chapters()
    print(f"Chapters ({len(chapters)}):")
    print(*chapters[:5], sep="\n")
    print("...")
    print(*chapters[-5:], sep="\n")
    """
    Chapters (400):
    Chapter(title='Глава 383. Неведение безначально', url='https://com-x.life/reader/2789/741667', pages=24, date=datetime.date(2025, 9, 11))
    Chapter(title='Глава 382. Усыпальница', url='https://com-x.life/reader/2789/719111', pages=22, date=datetime.date(2025, 6, 26))
    Chapter(title='Глава 381. Полумесяц освещающий спину изгнанника', url='https://com-x.life/reader/2789/715388', pages=23, date=datetime.date(2025, 6, 13))
    Chapter(title='Глава 380. Тени умирают дважды.', url='https://com-x.life/reader/2789/662311', pages=20, date=datetime.date(2025, 2, 28))
    Chapter(title='379', url='https://com-x.life/reader/2789/656178', pages=22, date=datetime.date(2025, 2, 14))
    ...
    Chapter(title='Том 2. Глава 0D Хранители желаний II', url='https://com-x.life/reader/2789/417510', pages=125, date=datetime.date(2024, 2, 15))
    Chapter(title='Том 1. Глава 0С Хранители желаний I', url='https://com-x.life/reader/2789/417509', pages=60, date=datetime.date(2024, 2, 15))
    Chapter(title='Том 1. Глава 0B Клеймо', url='https://com-x.life/reader/2789/417508', pages=69, date=datetime.date(2024, 2, 15))
    Chapter(title='Том 1. Глава 0А Чёрный Мечник', url='https://com-x.life/reader/2789/417507', pages=96, date=datetime.date(2024, 2, 15))
    Chapter(title='Том 1. Глава 00 Прототип', url='https://com-x.life/reader/2789/417459', pages=46, date=datetime.date(2024, 2, 14))
    """
