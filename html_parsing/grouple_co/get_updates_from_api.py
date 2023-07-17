#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import session, load


def get_feeds_by_manga_chapters() -> list[str]:
    # Auth and load
    rs = load("https://grouple.co/private/bookmarks/index#")

    data = {
        "bookmarkSort": "NAME",
        "elementFilter": [],
        "statusFilter": ["ANOTHER_UPDATES"],
        "includeUpdates": True,
        "limit": 50,
        "offset": 0,
    }

    session.headers.update(
        {
            "Authorization": f'Bearer {session.cookies["gwt"]}',
            "Referer": rs.url,
        }
    )

    rs = session.post("https://grouple.co/api/bookmark/activitiesList", json=data)
    rs.raise_for_status()

    return [
        f'{item["element"]["name"]} {item["title"]}'
        for item in rs.json()["list"]
    ]


if __name__ == "__main__":
    items = get_feeds_by_manga_chapters()
    print(f"Items ({len(items)}):", items)
