#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"

import market.models
from market.db import db, UserRoleEnum
from market.models import User, Product, ShoppingCart
from market import schemas


class Converter:
    @classmethod
    def get_GetUserModel(cls, user: User) -> market.models.GetUserModel:
        return market.models.GetUserModel(
            id=user.id,
            role=user.role,
            username=user.username,
        )

    @classmethod
    def get_GetProductModel(cls, product: Product) -> market.models.GetProductModel:
        return market.models.GetProductModel(
            id=product.id,
            name=product.name,
            price_minor=product.price_minor,
            description=product.description,
        )

    @classmethod
    def get_GetShoppingCartModel(
        cls,
        shopping_cart: ShoppingCart,
    ) -> market.models.GetShoppingCartModel:
        return market.models.GetShoppingCartModel(
            id=shopping_cart.id,
            product_ids=shopping_cart.product_ids,
        )


def get_users() -> market.models.GetUsersModel:
    return market.models.GetUsersModel(
        items=[Converter.get_GetUserModel(user) for user in db.get_users()]
    )


def get_user(id: str) -> market.models.GetUserModel:
    return Converter.get_GetUserModel(
        user=db.get_user(id, check_exists=True),
    )


def get_user_by_username(username: str) -> User:
    return db.get_user_by_username(username, check_exists=True)


def create_user(
    role: UserRoleEnum,
    username: str,
    password: str,
) -> market.models.IdBasedObjModel:
    user = db.create_user(
        role=role,
        username=username,
        password=password,
    )
    return market.models.IdBasedObjModel(id=user.id)


def get_products() -> market.models.GetProductsModel:
    return market.models.GetProductsModel(
        items=[Converter.get_GetProductModel(product) for product in db.get_products()]
    )


def get_product(id: str) -> market.models.GetProductModel:
    return Converter.get_GetProductModel(
        product=db.get_product(id, check_exists=True),
    )


def create_product(
    name: str,
    price_minor: int,  # Копейки
    description: str,
) -> market.models.IdBasedObjModel:
    product = db.create_product(
        name=name,
        price_minor=price_minor,
        description=description,
    )
    return market.models.IdBasedObjModel(id=product.id)


def create_shopping_cart(product_ids: list[str] = None) -> market.models.IdBasedObjModel:
    if product_ids is None:
        product_ids = []

    shopping_cart = db.create_shopping_cart(
        product_ids=product_ids,
    )
    return market.models.IdBasedObjModel(id=shopping_cart.id)


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


def get_shopping_carts() -> market.models.GetShoppingCartsModel:
    return market.models.GetShoppingCartsModel(
        items=[
            Converter.get_GetShoppingCartModel(obj) for obj in db.get_shopping_carts()
        ]
    )


def get_shopping_cart(id: str) -> market.models.GetShoppingCartModel:
    return Converter.get_GetShoppingCartModel(
        shopping_cart=db.get_shopping_cart(id, check_exists=True),
    )


def login(
    username: str,
    password: str,
) -> User | None:
    users = db.get_users(username=username, password=password)
    if users:
        return users[0]
