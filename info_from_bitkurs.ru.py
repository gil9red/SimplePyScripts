#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import grab


URL = "http://bitkurs.ru/"

# Copy page yandex
# URL = 'http://hghltd.yandex.net/yandbtm?fmode=inject&url=http%3A%2F%2Fbitkurs.ru%2F&tld=ru&lang=ru&la=1453455360&tm=1454924280&text=bitkurs.ru&l10n=ru&mime=html&sign=2105e628b413520a0e087ae4ac0db180&keyno=0'

g = grab.Grab()
g.setup(proxy="proxy.compassplus.ru:3128", proxy_type="http")
g.go(URL)

# <div class='currency_block'>
# <span class="btc_c currencies">1 BTC =</span>
# <span class="usd_c currencies">&#36;397.16<img src="/template/images/down.png"></span>
# <span class="rub_c currencies">19 862.57 руб.<img src="/template/images/down.png">
# </span><span class="eur_c currencies">366.51 &euro

usd = g.doc.select('//span[@class="usd_c currencies"]').text()
rub = g.doc.select('//span[@class="rub_c currencies"]').text()
eur = g.doc.select('//span[@class="eur_c currencies"]').text()


def get_amt(text):
    # Удаление всех символов, кроме цифр и точки
    text = re.sub(r"[^\d.]+", "", text)

    # Вытаскивание строки, описывающей число
    text = re.search(r"\d+(\.\d*)?", text).group()
    return text


usd = get_amt(usd)
rub = get_amt(rub)
eur = get_amt(eur)

print(f"1 BTC:\n  {usd} USD\n  {rub} RUB\n  {eur} EUR")
