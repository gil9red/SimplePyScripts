#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations


from playhouse.migrate import *


# TODO: имя в конфиг
DB_NAME = "../tracked_products.sqlite"


my_db = SqliteDatabase(DB_NAME)
migrator = SqliteMigrator(my_db)


with my_db.atomic():
    migrate(
        migrator.rename_column("price", "value", "value_dns"),
        migrator.add_column("price", "value_technopoint", DecimalField(null=True)),
        migrator.drop_index("price", "price_product_id_date_value"),
        migrator.add_index(
            "price",
            ("product_id", "date", "value_dns", "value_technopoint"),
            unique=True,
        ),
    )
