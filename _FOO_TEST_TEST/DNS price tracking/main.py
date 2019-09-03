#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
import time
from typing import Optional

from bs4 import BeautifulSoup
import requests
from peewee import *

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
import sys
sys.path.append('../../wait')

from wait import wait


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


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    title = TextField()
    url = TextField(unique=True)

    def get_last_price(self):
        last_price = self.prices.order_by(Price.date.desc()).first()
        if not last_price:
            return

        return last_price.value

    def append_price(self, value):
        Price.create(product=self, value=value)

    def __str__(self):
        return f'Product(title={repr(self.title)}, last_price={self.get_last_price()}, url={repr(self.url)})'


class Price(BaseModel):
    value = DecimalField(null=True)
    date = DateField(default=DT.datetime.now)
    product = ForeignKeyField(Product, backref='prices')

    class Meta:
        indexes = (
            (("product_id", "date"), True),
        )

    def __str__(self):
        return f'Price(value={self.value}, date={self.date}, product_id={self.product.id})'


db.connect()
db.create_tables([Product, Price])


checked_products = []


while True:
    checked_products.clear()

    try:
        for product_data in json.load(open('tracked_products.json', encoding='utf-8')):
            if product_data in checked_products:
                print(f"Duplicate: {repr(product_data['title'])}, url: {product_data['url']}\n")
                continue

            product, _ = Product.get_or_create(title=product_data['title'], url=product_data['url'])
            print(product)

            last_price = product.get_last_price()

            current_price = get_price(product.url)
            print(f'Current price: {current_price}')

            # Добавляем новую цену, если цена отличается или у продукта еще нет цен
            if current_price != last_price or not product.prices.count():
                print(f'Append new price: {current_price}')
                product.append_price(current_price)

            print()

            checked_products.append(product_data)

            time.sleep(5)  # 5 seconds

        wait(days=1)

    except Exception as e:
        # Выводим ошибку в консоль
        import traceback
        tb = traceback.format_exc()
        print(tb)

        print('Wait 15 minutes')
        time.sleep(15 * 60)  # 15 minutes
