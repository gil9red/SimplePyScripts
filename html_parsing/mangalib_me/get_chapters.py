#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from typing import Any, Self
from urllib.parse import urlparse

import requests


HOST_API: str = "https://api.cdnlibs.org"

session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0"


@dataclass
class Cover:
    filename: str
    thumbnail: str
    default: str
    md: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            filename=data["filename"],
            thumbnail=data["thumbnail"],
            default=data["default"],
            md=data["md"],
        )


@dataclass
class Team:
    id: int
    slug: str
    slug_url: str
    model: str
    name: str
    cover: Cover

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            slug=data["slug"],
            slug_url=data["slug_url"],
            model=data["model"],
            name=data["name"],
            cover=Cover.from_dict(data["cover"]),
        )


@dataclass
class User:
    id: int
    username: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            username=data["username"],
        )


@dataclass
class RestrictedView:
    is_open: bool
    expired_at: str
    price: int | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            is_open=data["is_open"],
            expired_at=data["expired_at"],
            price=data["price"],
        )


@dataclass
class Branch:
    id: int
    branch_id: int
    created_at: str
    teams: list[Team]
    expired_type: int
    user: User
    restricted_view: RestrictedView | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        rv_data = data.get("restricted_view")
        return cls(
            id=data["id"],
            branch_id=data["branch_id"],
            created_at=data["created_at"],
            teams=[Team.from_dict(t) for t in data["teams"]],
            expired_type=data["expired_type"],
            user=User.from_dict(data["user"]),
            restricted_view=RestrictedView.from_dict(rv_data) if rv_data else None,
        )


@dataclass
class Chapter:
    id: int
    index: int
    item_number: int
    volume: str
    number: str
    number_secondary: str
    name: str
    title: str
    url: str
    branches_count: int
    branches: list[Branch]
    bundle_id: int | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        host: str,
        lang: str,
        manga_slug: str,
    ) -> Self:
        branches: list[Branch] = [Branch.from_dict(b) for b in data.get("branches", [])]

        name: str = data["name"]
        volume: str = data["volume"]
        number: str = data["number"]
        url: str = f"{host}/{lang}/{manga_slug}/read/v{volume}/c{number}"

        is_locked: bool = branches and branches[0].restricted_view is not None
        status: str = "🔒 " if is_locked else ""
        title: str = f"{status}Том {volume} Глава {number}"
        if name:
            title = f"{title} - {name}"

        return cls(
            id=data["id"],
            index=data["index"],
            item_number=data["item_number"],
            volume=volume,
            number=number,
            number_secondary=data["number_secondary"],
            name=name,
            title=title,
            url=url,
            branches_count=data["branches_count"],
            branches=branches,
            bundle_id=data["bundle_id"],
        )


def get_chapters(url: str) -> list[Chapter]:
    result = urlparse(url)
    host: str = f"{result.scheme}://{result.netloc}"

    # Example: "/ru/manga/1234--foo" -> lang="ru", slug="1234--foo"
    uri: str = result.path.strip("/")
    lang: str = uri.split("/")[0]
    slug: str = uri.split("/")[-1]

    url_api: str = f"{HOST_API}/api/manga/{slug}/chapters"

    headers = {
        "Referer": host,
        "Content-Type": "application/json",
        "Origin": host,
    }
    rs = session.get(url_api, headers=headers)
    rs.raise_for_status()

    data: list[dict[str, Any]] = rs.json()["data"]
    return [
        Chapter.from_dict(item, host=host, lang=lang, manga_slug=slug) for item in data
    ]


if __name__ == "__main__":
    import time

    def _get_chapters(chapters: list[Chapter]) -> list[str]:
        return [f"    {c.title}: {c.url}" for c in chapters]

    for url in [
        "https://mangalib.me/ru/manga/12123--mieru-ko-chan",
        "https://mangalib.me/ru/manga/206--one-piece?from=catalog",
        "https://mangalib.me/ru/manga/162253--geim-sog-babalian-eulo-sal-anamgi?from=catalog&section=chapters&ui=5961682",
    ]:
        print(url)

        chapters: list[Chapter] = get_chapters(url)
        print(f"Chapters ({len(chapters)}):")
        print(*_get_chapters(chapters[:5]), sep="\n")
        print("    ...")
        print(*_get_chapters(chapters[-5:]), sep="\n")
        print()

        time.sleep(1)
    """
    https://mangalib.me/ru/manga/12123--mieru-ko-chan
    Chapters (80):
        Том 1 Глава 1: https://mangalib.me/ru/12123--mieru-ko-chan/read/v1/c1
        Том 1 Глава 2: https://mangalib.me/ru/12123--mieru-ko-chan/read/v1/c2
        Том 1 Глава 3: https://mangalib.me/ru/12123--mieru-ko-chan/read/v1/c3
        Том 1 Глава 4: https://mangalib.me/ru/12123--mieru-ko-chan/read/v1/c4
        Том 1 Глава 5: https://mangalib.me/ru/12123--mieru-ko-chan/read/v1/c5
        ...
        Том 13 Глава 65: https://mangalib.me/ru/12123--mieru-ko-chan/read/v13/c65
        Том 13 Глава 66: https://mangalib.me/ru/12123--mieru-ko-chan/read/v13/c66
        Том 13 Глава 67: https://mangalib.me/ru/12123--mieru-ko-chan/read/v13/c67
        Том 13 Глава 68: https://mangalib.me/ru/12123--mieru-ko-chan/read/v13/c68
        Том 14 Глава 69: https://mangalib.me/ru/12123--mieru-ko-chan/read/v14/c69
    
    https://mangalib.me/ru/manga/206--one-piece?from=catalog
    Chapters (1184):
        Том 1 Глава 0 - Рассвет романтики: https://mangalib.me/ru/206--one-piece/read/v1/c0
        Том 1 Глава 0.5 - Strong World: https://mangalib.me/ru/206--one-piece/read/v1/c0.5
        Том 1 Глава 1 - На заре приключений: https://mangalib.me/ru/206--one-piece/read/v1/c1
        Том 1 Глава 2 - Луффи Соломенная шляпа: https://mangalib.me/ru/206--one-piece/read/v1/c2
        Том 1 Глава 3 - Первая встреча: Охотник на пиратов Зоро: https://mangalib.me/ru/206--one-piece/read/v1/c3
        ...
        Том 108 Глава 1174 - Сильнейшее чувство в мире: https://mangalib.me/ru/206--one-piece/read/v108/c1174
        Том 108 Глава 1175 - Нидхегг: https://mangalib.me/ru/206--one-piece/read/v108/c1175
        Том 108 Глава 1176 - С гордостью: https://mangalib.me/ru/206--one-piece/read/v108/c1176
        Том 108 Глава 1177 - Гнев: https://mangalib.me/ru/206--one-piece/read/v108/c1177
        Том 108 Глава 1178 - Кошмар закончился: https://mangalib.me/ru/206--one-piece/read/v108/c1178
    
    https://mangalib.me/ru/manga/162253--geim-sog-babalian-eulo-sal-anamgi?from=catalog&section=chapters&ui=5961682
    Chapters (146):
        Том 1 Глава 1: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v1/c1
        Том 1 Глава 2: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v1/c2
        Том 1 Глава 3: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v1/c3
        Том 1 Глава 4: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v1/c4
        Том 1 Глава 5: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v1/c5
        ...
        Том 3 Глава 142: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v3/c142
        🔒 Том 3 Глава 143: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v3/c143
        🔒 Том 3 Глава 144: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v3/c144
        🔒 Том 3 Глава 145: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v3/c145
        🔒 Том 3 Глава 146: https://mangalib.me/ru/162253--geim-sog-babalian-eulo-sal-anamgi/read/v3/c146
    """
