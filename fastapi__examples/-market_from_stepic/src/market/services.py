#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from market.models import User, Product, ShoppingCart
from market.db import db, NotFoundException


def get_users() -> list[User]:
    return db.get_users()


def get_products() -> list[Product]:
    return db.get_products()


def get_product(id: str) -> Product:
    return db.get_product(id, check_exists=True)


def create_product(
    name: str,
    price_minor: int,  # Копейки
    description: str,
) -> Product:
    return db.create_product(
        name=name, price_minor=price_minor, description=description
    )


def create_shopping_cart() -> ShoppingCart:
    return db.create_shopping_cart(
        product_ids=[],
    )


def add_product_in_shopping_cart(
    shopping_cart_id: str,
    product_id: str,
):
    return db.add_product_in_shopping_cart(
        shopping_cart_id=shopping_cart_id,
        product_id=product_id,
    )


def remove_product_from_shopping_cart(
    shopping_cart_id: str,
    product_id: str,
):
    return db.remove_product_from_shopping_cart(
        shopping_cart_id=shopping_cart_id,
        product_id=product_id,
    )


def get_shopping_carts() -> list[ShoppingCart]:
    return db.get_shopping_carts()


def get_shopping_cart(id: str) -> ShoppingCart | None:
    return db.get_shopping_cart(id, check_exists=True)


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
