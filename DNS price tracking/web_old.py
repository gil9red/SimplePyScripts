#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import os.path

from flask import Flask, render_template, send_from_directory

from common import get_tracked_products
from db import Product, Price


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    titles = [p['title'] for p in get_tracked_products() if p.get('visible')]

    products = [
        (
            p.id, p.title, p.get_last_price_dns(), p.get_last_price_technopoint(),
            p.url, p.get_technopoint_url()
        )
        for p in Product.select()
    ]
    prices = [(p.id, p.date, p.value_dns, p.value_technopoint, p.product_id) for p in Price.select()]
    return render_template('index_old.html', products=products, prices=prices)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.png'
    )


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(
        port=10010,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
