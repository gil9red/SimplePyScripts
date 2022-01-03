#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import sqlite3

from collections import Counter
from pathlib import Path
from typing import List

from jsonlz4_mozLz4 import mozlz4a


def get_sessionstore(file_name_session: Path) -> dict:
    with open(file_name_session, 'rb') as f:
        return mozlz4a.loads_json(f)


def get_tab_urls_from_sessionstore(sessionstore: dict) -> List[str]:
    urls = []
    for w in sessionstore['windows']:
        for t in w['tabs']:
            i = t['index'] - 1
            tab_url = t['entries'][i]['url']
            urls.append(tab_url)

    return urls


def get_tab_urls(file_name_session: Path) -> List[str]:
    json_data = get_sessionstore(file_name_session)
    return get_tab_urls_from_sessionstore(json_data)


def close_tabs(
        file_name_session: Path,
        urls: List[str],
        log: logging.Logger,
):
    modified = False

    json_data = get_sessionstore(file_name_session)
    for w in json_data['windows']:
        for t in reversed(w['tabs']):
            i = t['index'] - 1
            tab_url = t['entries'][i]['url']

            if tab_url in urls:
                w['tabs'].remove(t)

                log.info(f'Removing tab: {tab_url}')
                modified = True

    if modified:
        with open(file_name_session, 'wb') as f:
            mozlz4a.dumps_json(f, json_data)


def close_duplicate_tabs(
        file_name_session: Path,
        log: logging.Logger,
):
    json_data = get_sessionstore(file_name_session)
    urls = get_tab_urls_from_sessionstore(json_data)

    need_to_delete = {
        url: count - 1
        for url, count in Counter(urls).items()
        if count > 1
    }

    for w in json_data['windows']:
        for t in reversed(w['tabs']):
            i = t['index'] - 1
            tab_url = t['entries'][i]['url']

            if need_to_delete.get(tab_url, 0) > 0:
                w['tabs'].remove(t)
                need_to_delete[tab_url] -= 1

                log.info(f'Removed duplicate: {tab_url}')

    if need_to_delete:
        with open(file_name_session, 'wb') as f:
            mozlz4a.dumps_json(f, json_data)


def get_bookmark_urls(
        file_name_places: Path
) -> List[str]:
    connect = sqlite3.connect(file_name_places)
    sql = 'SELECT p.url FROM moz_bookmarks b, moz_places p WHERE p.id = b.fk'
    return [place_url for place_url, in connect.execute(sql)]


def close_bookmarks(
        file_name_places: Path,
        urls: List[str],
        log: logging.Logger,
):
    with sqlite3.connect(file_name_places) as connect:
        for url in urls:
            sql = 'SELECT id FROM moz_bookmarks WHERE fk = (SELECT id FROM moz_places WHERE url = ?)'
            result = connect.execute(sql, [url]).fetchone()
            if not result:
                continue

            log.info(f"Deleted bookmark for url: {url}")
            sql = 'DELETE FROM moz_bookmarks WHERE id = ?'
            bookmark_id = result[0]
            connect.execute(sql, [bookmark_id])
