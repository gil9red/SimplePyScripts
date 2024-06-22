#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from market import models
from market.db import db


def get_users() -> models.Users:
    return models.Users(
        items=[models.create_from(models.User, user) for user in db.get_users()]
    )


def get_user(id: str) -> models.User:
    return models.create_from(
        models.User,
        db.get_user(id, check_exists=True),
    )


def get_user_by_username(username: str) -> models.UserInDb:
    return db.get_user_by_username(username, check_exists=True)


def create_user(
    role: models.UserRoleEnum,
    username: str,
    password: str,
) -> models.IdBasedObj:
    user = db.create_user(
        role=role,
        username=username,
        password=password,
    )
    return models.IdBasedObj(id=user.id)


def get_products() -> models.Products:
    return models.Products(items=db.get_products())


def get_product(id: str) -> models.Product:
    return db.get_product(id, check_exists=True)


def create_product(
    name: str,
    price_minor: int,  # Копейки
    description: str,
) -> models.IdBasedObj:
    product = db.create_product(
        name=name,
        price_minor=price_minor,
        description=description,
    )
    return models.IdBasedObj(id=product.id)


def update_product(
    id: str,
    name: str | None = None,
    price_minor: int | None = None,  # Копейки
    description: str | None = None,
):
    db.update_product(
        id=id,
        name=name,
        price_minor=price_minor,
        description=description,
    )


def create_shopping_cart(product_ids: list[str] = None) -> models.IdBasedObj:
    if product_ids is None:
        product_ids = []

    shopping_cart = db.create_shopping_cart(
        product_ids=product_ids,
    )
    return models.IdBasedObj(id=shopping_cart.id)


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


def get_shopping_carts() -> models.ShoppingCarts:
    return models.ShoppingCarts(items=db.get_shopping_carts())


def get_shopping_cart(id: str) -> models.ShoppingCart:
    return db.get_shopping_cart(id, check_exists=True)


def get_orders() -> models.Orders:
    return models.Orders(items=db.get_orders())


def get_order(id: str) -> models.Order:
    return db.get_order(id, check_exists=True)


def create_order(
    email: str,
    shopping_cart_id: str,
) -> models.IdBasedObj:
    obj = db.create_order(
        email=email,
        shopping_cart_id=shopping_cart_id,
    )
    return models.IdBasedObj(id=obj.id)
