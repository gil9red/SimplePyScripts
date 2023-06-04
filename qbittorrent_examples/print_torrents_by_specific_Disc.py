#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_client, print_torrents


qb = get_client()
need_disc = "E:"
torrents = [x for x in qb.torrents() if x["save_path"].startswith(need_disc)]
print_torrents(torrents)
