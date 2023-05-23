#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

import requests
from bs4 import BeautifulSoup


URL = "https://rpcs3.net/compatibility"


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"

page = last_page = 1
params = dict()
while page <= last_page:
    if page > 1:
        params["p"] = page

    rs = session.get(URL, params=params)
    root = BeautifulSoup(rs.content, "html.parser")

    for row_el in root.select("label.compat-table-row"):
        game_ids_el, game_title_el, status_el, _ = row_el.select(".compat-table-cell")

        game_ids = ", ".join(a.text for a in game_ids_el.select("a"))
        game_title = game_title_el.get_text(strip=True)
        status = status_el.get_text(strip=True)

        print(
            f"[page {page}] game_ids={game_ids!r}, game_title={game_title!r}, status={status}"
        )

    last_el = root.select_one(".compat-con-pages > a:last-child")
    last_page = int(last_el.text)
    page += 1

    time.sleep(5)

"""
[page 1] game_ids='NPUB31857', game_title='#KillAllZombies', status=Playable
[page 1] game_ids='BLJM61131', game_title="'&' - Sora no Mukou de Sakimasu you ni", status=Playable
[page 1] game_ids='NPUA80008', game_title='.detuned', status=Playable
[page 1] game_ids='BLJS93008', game_title='.hack//Versus', status=Playable
[page 1] game_ids='NPEB00026, NPUB30024', game_title='1942: Joint Strike', status=Playable
[page 1] game_ids='NPEB90079, NPUB90104', game_title='1942: Joint Strike Trial', status=Playable
[page 1] game_ids='NPUB90369', game_title='2010 FIFA World Cup', status=Playable
[page 1] game_ids='BLES00796, BLUS30474', game_title='2010 FIFA World Cup: South Africa', status=Playable
[page 1] game_ids='BLES01994, BLUS31389', game_title='2014 FIFA World Cup Brazil', status=Playable
[page 1] game_ids='NPEB01947', game_title='2014 FIFA World Cup Brazil', status=Playable
[page 1] game_ids='NPEB90528', game_title='2014 FIFA World Cup Brazil Demo', status=Playable
[page 1] game_ids='NPEB00080, NPJB00019, NPUB30058', game_title='3 on 3 NHL Arcade', status=Playable
[page 1] game_ids='NPIA00008', game_title='30 things you can do with PS3', status=Playable
[page 1] game_ids='BLJM60180', game_title='3D Dot Game Heroes', status=Playable
[page 1] game_ids='NPEB00287, NPUB30156', game_title='3D Ultra MiniGolf Adventures 2', status=Playable
[page 1] game_ids='NPUB30347', game_title='4 Elements HD', status=Playable
[page 1] game_ids='BLJS10057', game_title='428: Fuusa Sareta Shibuya de', status=Playable
[page 1] game_ids='NPEB01397', game_title='4K Gallery', status=Playable
[page 1] game_ids='BLES00472, BLUS30256', game_title='50 Cent: Blood on the Sand', status=Playable
[page 1] game_ids='BLJS10056', game_title='50 Cent: Blood On The Sand', status=Playable
[page 1] game_ids='NPEB02164', game_title='A Boy and His Blob', status=Playable
[page 1] game_ids='NPEB01127, NPUB30878', game_title='A-Men', status=Playable
[page 1] game_ids='NPEB01210', game_title='A-Men 2', status=Playable
[page 1] game_ids='NPEB01872, NPUB31365', game_title='Aabs Animals', status=Playable
[page 1] game_ids='NPEB02133', game_title="Aaru's Awakening", status=Playable
"""
