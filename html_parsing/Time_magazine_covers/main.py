#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
import re
import shutil
import traceback

from os import makedirs
from os.path import abspath, normpath
from urllib.request import urlretrieve
from typing import List, Union, NamedTuple

import requests


class Cover(NamedTuple):
    title: str
    url: str


def parse_date(date_str: str) -> DT.date:
    fmts = (
        '%B %d, %Y',
        '%b %d, %Y',
    )
    for fmt in fmts:
        try:
            return DT.datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass

    raise ValueError(f'Unknown date format for "{date_str}"')


def get_covers(year: Union[int, str]) -> List[Cover]:
    items = []

    try:
        url = f'https://time.com/vault/year/{year}/'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        }

        session = requests.session()
        session.headers.update(headers)

        rs = session.get(url)
        if not rs.ok:
            raise Exception(f'Something went wrong...: status_code: {rs.status_code}'
                            f'\nUrl: {url}\nRs.Url: {rs.url}\n{rs.text}')

        match = re.search(r'<script>Time\.bootstrap = ({.+})</script>', rs.text)
        if not match:
            raise Exception(f'Not found "Time.bootstrap = ...): status_code: {rs.status_code}'
                            f'\nUrl: {url}\nRs.Url: {rs.url}\n{rs.text}"')

        result = json.loads(match.group(1), encoding=rs.encoding)
        if 'vault' not in result:
            raise Exception(f'Field "vault" not found in result: status_code: {rs.status_code}'
                            f'\nUrl: {url}\nRs.Url: {rs.url}'
                            f'\nResult: {result}\nHtml:\n{rs.text}')

        for vault in result['vault']:
            cover_date = parse_date(vault['date'])
            items.append(
                Cover(
                    title=f"Cover_{cover_date:%Y-%m-%d}",
                    url=vault['hero']['src']['large']
                )
            )

    except Exception:
        print(f'[-] {traceback.format_exc()}')

    return items


def dump_covers(year: Union[str, int], out_dir='out', need_zip=False, remove_out_covers=False):
    covers = get_covers(year)
    out_dir = normpath(abspath(out_dir + f"/{year}"))

    print(f'Dump {len(covers)} covers to {out_dir!r}')
    makedirs(out_dir, exist_ok=True)

    for x in covers:
        urlretrieve(x.url, f'{out_dir}/{x.title}.jpg')

    if need_zip:
        print(f'Make archive from {out_dir!r}')
        zip_name = shutil.make_archive(out_dir, 'zip', root_dir=out_dir)
        print(f'Finish make archive to {zip_name!r}')

        if remove_out_covers:
            print(f'Remove {out_dir!r}')
            shutil.rmtree(out_dir)


if __name__ == '__main__':
    YEAR = DT.datetime.now().year

    items = get_covers(YEAR)
    print(f'Covers for {YEAR} year ({len(items)}):')

    for x in items:
        print(f'    {x.title}: {x.url}')

    # Covers (39):
    #     Cover_140119: https://api.time.com/wp-content/uploads/2019/01/TIM190114v1.jpg?quality=85&w=550
    #     Cover_210119: https://api.time.com/wp-content/uploads/2019/01/pelositrumpjan21cover.jpg?quality=85&w=550
    #     Cover_280119: https://api.time.com/wp-content/uploads/2019/01/tim190128v1_tech.cover_.jpg?quality=85&w=550
    #     Cover_040219: https://api.time.com/wp-content/uploads/2019/01/0204intcover.jpg?quality=85&w=550
    #     Cover_180219: https://api.time.com/wp-content/uploads/2019/02/cicely.cover_.final_.jpg?quality=85&w=550
    #     Cover_040319: https://api.time.com/wp-content/uploads/2019/02/tim190304v1_2020.coverfinal.jpg?quality=85&w=550
    #     ...
    #     Cover_181119: https://api.time.com/wp-content/uploads/2019/11/tim191118v1_impeach.cover_.jpg?quality=85&w=550
    #     Cover_141119: https://api.time.com/wp-content/uploads/2019/11/time-100-next-covers-1.gif?w=550
    #     Cover_021219: https://api.time.com/wp-content/uploads/2019/11/tim191202v1_elites.cover2_.jpg?quality=85&w=550

    print()

    dump_covers(YEAR, need_zip=True)  # Out + zip
    # OR:
    # dump_covers(YEAR)  # Only out
    # OR:
    # dump_covers(YEAR, need_zip=True, remove_out_covers=True)  # Only zip
    # OR:
    # dump_covers(YEAR, out_dir='out_covers', need_zip=True, remove_out_covers=True)
