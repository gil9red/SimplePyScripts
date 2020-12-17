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

from common import get_tracked_products
from db import Product, db_create_backup


checked_products = []


while True:
    print(f'Started at {DT.datetime.now():%d/%m/%Y %H:%M:%S}\n')

    db_create_backup()

    checked_products.clear()

    try:
        for product_data in get_tracked_products():
            if product_data in checked_products:
                print(f"Duplicate: {repr(product_data['title'])}, url: {product_data['url']}\n")
                continue

            product, _ = Product.get_or_create(title=product_data['title'], url=product_data['url'])
            print(product)

            last_price_dns = product.get_last_price_dns(actual_price=False)
            print(f'DNS: {last_price_dns} / '
                  f'{product.get_last_price_dns(actual_price=True)} (actual)')

            last_price_technopoint = product.get_last_price_technopoint(actual_price=False)
            print(f'Technopoint: {last_price_technopoint} / '
                  f'{product.get_last_price_technopoint(actual_price=True)} (actual)')

            current_url_price_dns = get_price(product.url)
            current_url_price_technopoint = get_price(product.get_technopoint_url())
            print(f'Current url price: DNS={current_url_price_dns}, Technopoint={current_url_price_technopoint}')

            is_change_dns = current_url_price_dns != last_price_dns
            is_change_technopoint = current_url_price_technopoint != last_price_technopoint
            is_first_price = not product.prices.count()

            # Добавляем новую цену, если цена отличается или у продукта еще нет цен
            if is_change_dns or is_change_technopoint or is_first_price:
                text = f'Append new price: DNS={current_url_price_dns}, Technopoint={current_url_price_technopoint}.' \
                       f' Reason: '
                if is_first_price:
                    text += 'First price'
                else:
                    if is_change_dns and is_change_technopoint:
                        text += 'DNS and Technopoint'
                    elif is_change_dns:
                        text += 'DNS'
                    else:
                        text += 'Technopoint'
                print(text)

                product.append_price(current_url_price_dns, current_url_price_technopoint)

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
