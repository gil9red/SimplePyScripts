#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shelve

from market.models import User, Product, ShoppingCart, UserRole


class DB:
    KEY_USERS: str = "users"
    KEY_PRODUCTS: str = "products"
    KEY_SHOPPING_CARTS: str = "shopping_carts"

    db_name: str = "db"

    def __init__(self):
        with self.get_shelve() as db:
            db[self.KEY_USERS] = dict()
            db[self.KEY_PRODUCTS] = dict()
            db[self.KEY_SHOPPING_CARTS] = dict()

            if "admin" not in db[self.KEY_USERS]:
                admin = User(
                    # Это uuid4 – уникальный идентификатор пользователя
                    id="29ae7ebf-4445-42f2-9548-a3a54f095220",
                    role=UserRole.ADMIN,
                    username="admin",
                    password="Admin_4321!",
                )
                db[self.KEY_USERS][admin.id] = admin

            # TODO: products

    def get_shelve(self) -> shelve.Shelf:
        return shelve.open(self.db_name, writeback=True)

    def get_users(
        self,
        username: str | None = None,
        password: str | None = None,
    ) -> list[User]:
        """
        :param username: фильтр по логину
        :param password: фильтр по паролю
        :return: отфильтрованные пользователи
        """

        with self.get_shelve() as db:
            filtered_users = []  # Тут собираются отфильтрованные пользователи

            # Перебираем всех пользователей и оставляем только тех, кто прошел фильтры
            for user in db[self.KEY_USERS].values():
                if username is not None and user.username != username:
                    continue
                if password is not None and user.password != password:
                    continue
                filtered_users.append(user)

            return filtered_users

    def create_user(self, user: User):
        with self.get_shelve() as db:
            db[self.KEY_USERS][user.id] = user

    def create_product(self, product: Product):
        with self.get_shelve() as db:
            db[self.KEY_PRODUCTS][product.id] = product

    def get_products(self) -> list[Product]:
        with self.get_shelve() as db:
            return list(db[self.KEY_PRODUCTS].values())

    def create_shopping_cart(self, shopping_cart: ShoppingCart):
        with self.get_shelve() as db:
            db[self.KEY_SHOPPING_CARTS][shopping_cart.id] = shopping_cart

    def get_shopping_carts(self) -> list[ShoppingCart]:
        with self.get_shelve() as db:
            return list(db[self.KEY_SHOPPING_CARTS].values())

    def get_shopping_cart(self, id: str) -> ShoppingCart | None:
        with self.get_shelve() as db:
            return db[self.KEY_SHOPPING_CARTS].get(id)

    # TODO: Для добавления продукта нужен только id
    def add_product_in_shopping_cart(self, product: Product, shopping_cart: ShoppingCart):
        shopping_cart.products.append(product)
        # TODO: ?
        self.create_shopping_cart(shopping_cart)

    # TODO: Для удаления продукта нужен только id
    def remove_product_from_shopping_cart(self, product: Product, shopping_cart: ShoppingCart):
        shopping_cart.products.remove(product)
        # TODO: ?
        self.create_shopping_cart(shopping_cart)


db = DB()
