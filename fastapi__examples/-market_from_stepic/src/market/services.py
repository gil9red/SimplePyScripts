#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from market.db import db, UserRoleEnum
from market.models import User, Product, ShoppingCart
from market import schemas


class Converter:
    @classmethod
    def get_GetUserModel(cls, user: User) -> schemas.GetUserModel:
        return schemas.GetUserModel(
            id=user.id,
            role=user.role,
            username=user.username,
        )

    @classmethod
    def get_GetProductModel(cls, product: Product) -> schemas.GetProductModel:
        return schemas.GetProductModel(
            id=product.id,
            name=product.name,
            price_minor=product.price_minor,
            description=product.description,
        )

    @classmethod
    def get_GetShoppingCartModel(
        cls,
        shopping_cart: ShoppingCart,
    ) -> schemas.GetShoppingCartModel:
        return schemas.GetShoppingCartModel(
            id=shopping_cart.id,
            product_ids=shopping_cart.product_ids,
        )


def get_users() -> schemas.GetUsersModel:
    return schemas.GetUsersModel(
        items=[Converter.get_GetUserModel(user) for user in db.get_users()]
    )


def get_user(id: str) -> schemas.GetUserModel:
    return Converter.get_GetUserModel(
        user=db.get_user(id, check_exists=True),
    )


def create_user(
    role: UserRoleEnum,
    username: str,
    password: str,
) -> schemas.IdBasedObjModel:
    user = db.create_user(
        role=role,
        username=username,
        password=password,
    )
    return schemas.IdBasedObjModel(id=user.id)


def get_products() -> schemas.GetProductsModel:
    return schemas.GetProductsModel(
        items=[Converter.get_GetProductModel(product) for product in db.get_products()]
    )


def get_product(id: str) -> schemas.GetProductModel:
    return Converter.get_GetProductModel(
        product=db.get_product(id, check_exists=True),
    )


def create_product(
    name: str,
    price_minor: int,  # Копейки
    description: str,
) -> schemas.IdBasedObjModel:
    product = db.create_product(
        name=name,
        price_minor=price_minor,
        description=description,
    )
    return schemas.IdBasedObjModel(id=product.id)


def create_shopping_cart(product_ids: list[str] = None) -> schemas.IdBasedObjModel:
    if product_ids is None:
        product_ids = []

    shopping_cart = db.create_shopping_cart(
        product_ids=product_ids,
    )
    return schemas.IdBasedObjModel(id=shopping_cart.id)


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


def get_shopping_carts() -> schemas.GetShoppingCartsModel:
    return schemas.GetShoppingCartsModel(
        items=[
            Converter.get_GetShoppingCartModel(obj) for obj in db.get_shopping_carts()
        ]
    )


def get_shopping_cart(id: str) -> schemas.GetShoppingCartModel:
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
