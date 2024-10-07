#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import session, do_post, load


def get_feeds_by_manga_chapters() -> list[str]:
    # Auth and load
    rs = load("/private/bookmarks/index#")

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

    rs = do_post("/api/bookmark/activitiesList", json=data)
    return [
        f'{item["element"]["name"]} {item["title"]}'
        for item in rs.json()["list"]
        if item["type"] == "CHAPTER_NEW"
    ]


if __name__ == "__main__":
    items = get_feeds_by_manga_chapters()
    print(f"Items ({len(items)}):", items)
