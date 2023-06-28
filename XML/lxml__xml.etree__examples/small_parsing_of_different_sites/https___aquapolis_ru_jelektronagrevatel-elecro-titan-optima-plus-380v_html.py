#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from lxml import html


rs = requests.get(
    "https://aquapolis.ru/jelektronagrevatel-elecro-titan-optima-plus-380v.html"
)
root = html.fromstring(rs.content)


def get_text(node):
    return html.tostring(node, method="text", encoding="unicode").strip()


for tr in root.cssselect("#super-product-table tr"):
    tds = tr.cssselect("td")
    if not tds:
        continue

    name = get_text(tds[0])
    price = get_text(tds[1].cssselect(".price-box > .regular-price > .price")[0])

    value = tds[2].cssselect("input")[0].get("value")
    stock_status = "Нет в наличии" if value == "0" else "Есть"

    print(f"{name:65} | {price:16} | {stock_status}")


# Электронагреватель Elecro Titan Optima Plus СP-18 18 кВт (380В)   | 211 572,00 руб.  | Есть
# Электронагреватель Elecro Titan Optima Plus СP-24 24 кВт (380В)   | 214 638,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-30 30 кВт (380В)   | 217 704,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-36 36 кВт (380В)   | 229 970,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-45 45 кВт (380В)   | 248 367,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-54 54 кВт (380В)   | 251 433,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-60 60 кВт (380В)   | 285 162,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-72 72 кВт (380В)   | 294 361,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-96 96 кВт (380В)   | 358 753,00 руб.  | Нет в наличии
# Электронагреватель Elecro Titan Optima Plus СP-120 120 кВт (380В) | 397 080,00 руб.  | Нет в наличии
