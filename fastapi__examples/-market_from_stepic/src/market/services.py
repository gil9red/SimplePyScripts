#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO:
from uuid import uuid4

from market.models import User, Product, ShoppingCart
from market.db import db


def get_users() -> list[User]:
    return db.get_users()


def get_products() -> list[Product]:
    return db.get_products()


def create_product(
        name: str,
        price_minor: int,  # Копейки
        description: str,
) -> Product:
    # TODO: Несколько странно, что Product создается вне базы
    #       Нужно бы внутрь базы перенести
    obj = Product(
        id=str(uuid4()),
        name=name,
        price_minor=price_minor,
        description=description
    )
    db.create_product(obj)

    return obj


def get_shopping_carts() -> list[ShoppingCart]:
    return db.get_shopping_carts()


def get_shopping_cart(id: str) -> ShoppingCart | None:
    return db.get_shopping_cart(id)


#
# def create_article(
#     title: str, content: str, articles_repository: ArticlesRepository
# ) -> Article:
#     article = Article(id=str(uuid4()), title=title, content=content)
#     articles_repository.create_article(article=article)
#     return article


def login(
    username: str,
    password: str,
) -> User | None:
    users = db.get_users(username=username, password=password)
    if users:
        return users[0]
