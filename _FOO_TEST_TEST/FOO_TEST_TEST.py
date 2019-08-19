#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
from typing import Optional
import time

from peewee import *
from bs4 import BeautifulSoup
import requests


def wait(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    from datetime import timedelta, datetime
    today = datetime.today()
    timeout_date = today + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )

    while today <= timeout_date:
        def str_timedelta(td):
            # Remove ms
            td = str(td)
            if '.' in td:
                td = td[:td.index('.')]

            return td

        left = timeout_date - today
        left = str_timedelta(left)

        print('\r' * 100, end='')
        print('До следующего запуска осталось {}'.format(left), end='')

        import sys
        sys.stdout.flush()

        # Delay 1 seconds
        import time
        time.sleep(1)

        today = datetime.today()

    print('\r' * 100, end='')
    print('\n')


def get_price(url: str) -> Optional[int]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    }

    rs = requests.get(url, headers=headers)

    root = BeautifulSoup(rs.content, 'html.parser')
    price_value = root.select_one('.current-price-value')
    if not price_value:
        return

    return int(price_value['data-price-value'])


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase('tracked_products.sqlite', pragmas={'foreign_keys': 1})


class Product(Model):
    title = TextField()
    url = TextField(unique=True)

    def get_last_price(self):
        last_price = self.prices.order_by(Price.date.desc()).first()
        if last_price:
            last_price = last_price.value

        return last_price

    class Meta:
        database = db


class Price(Model):
    value = DecimalField(null=True)
    date = DateField(default=DT.datetime.now)
    product = ForeignKeyField(Product, backref='prices')

    class Meta:
        database = db

        indexes = (
            (("product_id", "date"), True),
        )


db.connect()
db.create_tables([Product, Price])

while True:
    try:
        for product_data in json.load(open('tracked_products.json', encoding='utf-8')):
            product, _ = Product.get_or_create(title=product_data['title'], url=product_data['url'])
            last_price = product.get_last_price()

            print(product.title, product.url, last_price)

            current_price = get_price(product.url)
            print('current price:', current_price)

            # Цена отличается или у продукта еще нет цен
            if current_price != last_price or not product.prices.count():
                print('Append new price')
                Price.get_or_create(product=product, value=current_price)

            print()

            time.sleep(5)  # 5 seconds

            # last_price = product.prices.order_by(Price.date.desc()).first()
            # print(list(product.prices), last_price.value if last_price else None)
            #
            # #
            # # print(product.title, get_price(product.url))
            #
            # for price_data in product_data.get('prices', []):
            #     date = DT.datetime.strptime(price_data['date'], '%Y-%m-%d').date()
            #     print(date, price_data['date'])
            #
            #     last_price = product.prices.order_by(Price.date.desc()).first()
            #     if last_price:
            #         last_price = last_price.value
            #
            #     Price.get_or_create(product=product, value=price_data['value'], date=date)
            #
            # last_price = product.prices.order_by(Price.date.desc()).first()
            # print(list(product.prices), last_price.value if last_price else None)
            # print()

        wait(days=1)

    except Exception as e:
        # Выводим ошибку в консоль
        import traceback
        tb = traceback.format_exc()
        print(tb)

        time.sleep(15 * 60)  # 60 minutes
