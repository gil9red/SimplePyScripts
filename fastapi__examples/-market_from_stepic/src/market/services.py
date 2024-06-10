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


def get_shopping_carts() -> list[ShoppingCart]:
    return db.get_shopping_carts()


#
# def create_article(
#     title: str, content: str, articles_repository: ArticlesRepository
# ) -> Article:
#     article = Article(id=str(uuid4()), title=title, content=content)
#     articles_repository.create_article(article=article)
#     return article


def login(
    username: str, password: str
) -> User | None:
    users = db.get_users(username=username, password=password)
    if users:
        return users[0]
