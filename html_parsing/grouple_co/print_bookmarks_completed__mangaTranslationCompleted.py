#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import Status, get_bookmarks_by_status


items = get_bookmarks_by_status(Status.WATCHING)

print(f"Total bookmarks ({len(items)}):")
for x in items:
    print(f"    {x.title!r}: {x.url}")

print("\n")

completed = [x for x in items if "переведено" in x.tags]
print(f"Total bookmarks completed ({len(completed)}):")
for x in completed:
    print(f"    {x.title!r}: {x.url}")
