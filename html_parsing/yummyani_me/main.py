#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Self

import requests
from requests.exceptions import RequestException


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/99.0"


def do_get(url: str, **kwargs) -> requests.Response:
    timeout: float | None = kwargs.get("timeout")
    if timeout is None:
        kwargs["timeout"] = 30.0

    exc: Exception | None = None
    for _ in range(5):
        try:
            return session.get(url, **kwargs)
        except RequestException as e:  # NOTE: Были ошибки сети
            exc = e

    if exc:
        raise exc


@dataclass
class Episodes:
    count: int
    aired: int
    next_date_secs: int
    next_date: datetime

    @classmethod
    def parse(cls, data: dict[str, Any]) -> Self:
        next_date_secs: int = data["next_date"]

        return cls(
            count=data["count"],
            aired=data["aired"],
            next_date_secs=next_date_secs,
            next_date=datetime.fromtimestamp(next_date_secs),
        )


# TODO: Поддержать больше полей?
@dataclass
class Anime:
    title: str
    anime_url: str
    anime_id: int
    year: int
    description: str
    duration_secs: int
    anime_status_title: str
    genres: list[str] = field(default_factory=list)
    episodes: Episodes = field(default_factory=Episodes)
    other_titles: list[str] = field(default_factory=list)

    @classmethod
    def parse(cls, data: dict[str, Any]) -> Self:
        data = data["response"]

        return cls(
            title=data["title"],
            anime_url=data["anime_url"],
            anime_id=data["anime_id"],
            year=data["year"],
            description=data["description"],
            duration_secs=data["duration"],
            anime_status_title=data["anime_status"]["title"],
            genres=[obj["title"] for obj in data["genres"]],
            episodes=Episodes.parse(data["episodes"]),
            other_titles=data["other_titles"],
        )


def get_anime_by_url(url_or_name: str) -> Anime:
    # Учитываем, что url_or_name может быть ссылкой
    name: str = url_or_name.split("/")[-1]

    url: str = f"https://ru.yummyani.me/api/anime/{name}"

    rs = do_get(url)
    rs.raise_for_status()

    return Anime.parse(rs.json())


if __name__ == "__main__":
    anime = get_anime_by_url("https://site.yummyani.me/catalog/item/doktor-stoun-nauchnoe-buduschee-chast-2")
    print(anime)
    # Anime(title='Доктор Стоун: Научное будущее. Часть 2', anime_url='doktor-stoun-nauchnoe-buduschee-chast-2', anime_id=19654, year=2025, description='В один роковой день всё человечество превратилось в камень. Много тысячелетий спустя старшеклассник Тайдзю освобождается от окаменения и оказывается в окружении статуй. Однако он не одинок: его другу Сэнку также удалось сбросить каменную оболочку, и теперь, используя научные знания, они начинают восстанавливать былую цивилизацию.', duration_secs=10237, anime_status_title='онгоинг', genres=['Сёнэн', 'Комедия', 'Приключения', 'Фантастика'], episodes=Episodes(count=12, aired=7, next_date_secs=1756386000, next_date=datetime.datetime(2025, 8, 28, 18, 0)), other_titles=['Dr. Stone 4th Season Part 2', 'Dr. Stone: Science Future Part 2', 'Dr.STONE SCIENCE FUTURE 第2クール'])

    assert anime == get_anime_by_url("https://ru.yummyani.me/catalog/item/doktor-stoun-nauchnoe-buduschee-chast-2")
    assert anime == get_anime_by_url("doktor-stoun-nauchnoe-buduschee-chast-2")
