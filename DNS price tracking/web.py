#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import os.path
from decimal import Decimal
from typing import Optional

from flask import Flask, render_template, send_from_directory

from db import Product, Price


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_float(value: Decimal) -> Optional[float]:
    if value is None:
        return
    return float(value)


@app.route("/")
def index():
    products = []
    for p in Product.select():
        products.append({
            "recid": p.id,
            "title": p.title,
            "price_dns": get_float(p.get_last_price_dns()),
            "price_techopoint": get_float(p.get_last_price_technopoint()),
            "link_dns": p.url,
            "link_techopoint": p.get_technopoint_url(),
        })

    prices = dict()
    for p in Price.select():
        if p.product_id not in prices:
            prices[p.product_id] = []

        prices[p.product_id].append({
            "recid": p.id,
            "datetime": p.date.isoformat(),
            "price_dns": get_float(p.value_dns),
            "price_techopoint": get_float(p.value_technopoint),
        })

    return render_template('index.html', products=products, prices=prices)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.png'
    )


if __name__ == '__main__':
    app.debug = True

    app.run(
        port=10010
    )

    # # Public IP
    # app.run(host='0.0.0.0')
