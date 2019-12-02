#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
import time

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
import sys
sys.path.append('../wait')
sys.path.append('../html_parsing/www_dns_shop_ru')

from wait import wait
from get_price import get_price

from db import Product, db_create_backup


checked_products = []


while True:
    print(f'Started at {DT.datetime.now():%d/%m/%Y %H:%M:%S}\n')

    db_create_backup()

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

    print()
