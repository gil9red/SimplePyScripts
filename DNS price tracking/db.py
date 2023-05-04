#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import pathlib
import os
import shutil

from peewee import *

# Absolute file name
DB_FILE_NAME = str(pathlib.Path(__file__).resolve().parent / "tracked_products.sqlite")


def db_create_backup(backup_dir="backup"):
    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(DT.datetime.today().date()) + ".sqlite"
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    title = TextField()
    url = TextField(unique=True)

    def get_technopoint_url(self) -> str:
        return self.url.replace("www.dns-shop.ru", "technopoint.ru")

    def get_last_price_dns(self, actual_price=True):
        prices = self.prices

        # Возвращаем последнюю указанную цену (Price.value_dns != null)
        if actual_price:
            prices = prices.where(Price.value_dns.is_null(is_null=False))

        last_price = prices.order_by(Price.date.desc()).first()
        if not last_price:
            return

        return last_price.value_dns

    def get_last_price_technopoint(self, actual_price=True):
        prices = self.prices

        # Возвращаем последнюю указанную цену (Price.value_technopoint != null)
        if actual_price:
            prices = prices.where(Price.value_technopoint.is_null(is_null=False))

        last_price = prices.order_by(Price.date.desc()).first()
        if not last_price:
            return

        return last_price.value_technopoint

    def append_price(self, value_dns, value_technopoint):
        Price.create(
            product=self, value_dns=value_dns, value_technopoint=value_technopoint
        )

    def __str__(self):
        # TODO: выводить последнюю цену и актуальную
        return (
            f"Product(title={self.title!r}, "
            f"last_price_dns={self.get_last_price_dns()}, "
            f"last_price_technopoint={self.get_last_price_technopoint()}, "
            f"url={self.url!r})"
        )


class Price(BaseModel):
    value_dns = DecimalField(null=True)
    value_technopoint = DecimalField(null=True)
    date = DateTimeField(default=DT.datetime.now)
    product = ForeignKeyField(Product, backref="prices")

    class Meta:
        indexes = ((("product_id", "date", "value_dns", "value_technopoint"), True),)

    def __str__(self):
        return (
            f"Price(value_dns={self.value_dns}, "
            f"value_technopoint={self.value_technopoint}, "
            f"date={self.date}, product_id={self.product.id})"
        )


db.connect()
db.create_tables([Product, Price])


if __name__ == "__main__":
    for product in Product.select():
        print(product)

        for p in product.prices.select():
            print("   ", p)

        print()
