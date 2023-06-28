#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import traceback
import sys

from datetime import datetime

# pip install simple-wait
from simple_wait import wait

sys.path.append("../html_parsing/www_dns_shop_ru")
from get_price import get_price

from common import get_tracked_products
from db import Product, db_create_backup


checked_products = []


while True:
    print(f"Started at {datetime.now():%d/%m/%Y %H:%M:%S}\n")

    db_create_backup()

    checked_products.clear()

    try:
        for product_data in get_tracked_products():
            if product_data in checked_products:
                print(
                    f"Duplicate: {repr(product_data['title'])}, url: {product_data['url']}\n"
                )
                continue

            product, _ = Product.get_or_create(
                title=product_data["title"], url=product_data["url"]
            )
            print(product)

            last_price_dns = product.get_last_price_dns()
            last_price_technopoint = product.get_last_price_technopoint()
            print(f"Last DNS: {last_price_dns}, Technopoint: {last_price_technopoint}")

            current_url_price_dns = get_price(product.url)
            current_url_price_tp = get_price(product.get_technopoint_url())
            print(
                f"Current url price: DNS={current_url_price_dns}, Technopoint={current_url_price_tp}"
            )

            is_change_dns = current_url_price_dns and current_url_price_dns != last_price_dns
            is_change_technopoint = current_url_price_tp and current_url_price_tp != last_price_technopoint
            is_first_price = not product.prices.count()

            # Добавляем новую цену, если цена отличается или у продукта еще нет цен
            if is_change_dns or is_change_technopoint or is_first_price:
                text = (
                    f"Append new price: DNS={current_url_price_dns}, Technopoint={current_url_price_tp}."
                    f" Reason: "
                )
                if is_first_price:
                    text += "First price"
                else:
                    if is_change_dns and is_change_technopoint:
                        text += "DNS and Technopoint"
                    elif is_change_dns:
                        text += "DNS"
                    else:
                        text += "Technopoint"
                print(text)

                product.append_price(current_url_price_dns, current_url_price_tp)

            print()

            checked_products.append(product_data)

            time.sleep(5)  # 5 seconds

        wait(days=1)

    except Exception as e:
        # Выводим ошибку в консоль
        tb = traceback.format_exc()
        print(tb)

        print("Wait 15 minutes")
        wait(minutes=15)

    print()
