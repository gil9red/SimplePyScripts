#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

from peewee import *

# Absolute file name
import pathlib
DB_FILE_NAME = str(pathlib.Path(__file__).resolve().parent / 'tracked_products.sqlite')


def db_create_backup(backup_dir='backup'):
    import datetime as DT
    import os
    import shutil

    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(DT.datetime.today().date()) + '.sqlite'
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    title = TextField()
    url = TextField(unique=True)

    def get_last_price(self):
        # Возвращаем последнюю указанную цену (Price.value != null)
        last_price = self.prices.where(Price.value.is_null(is_null=False)).order_by(Price.date.desc()).first()
        if not last_price:
            return

        return last_price.value

    def append_price(self, value):
        Price.create(product=self, value=value)

    def __str__(self):
        return f'Product(title={repr(self.title)}, last_price={self.get_last_price()}, url={repr(self.url)})'


class Price(BaseModel):
    value = DecimalField(null=True)
    date = DateTimeField(default=DT.datetime.now)
    product = ForeignKeyField(Product, backref='prices')

    class Meta:
        indexes = (
            (("product_id", "date", "value"), True),
        )

    def __str__(self):
        return f'Price(value={self.value}, date={self.date}, product_id={self.product.id})'


db.connect()
db.create_tables([Product, Price])


if __name__ == '__main__':
    for product in Product.select():
        print(product)

        for p in product.prices.select():
            print('   ', p)

        print()
