#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shelve
from uuid import uuid4

from market.config import DB_FILE_NAME
from market.models import User, Product, ShoppingCart, UserRole


class DB:
    KEY_USERS: str = "users"
    KEY_PRODUCTS: str = "products"
    KEY_SHOPPING_CARTS: str = "shopping_carts"

    db_name: str = str(DB_FILE_NAME)

    def _do_init_db_objects(self):
        with self.get_shelve() as db:
            print(dict(db))

            if self.KEY_USERS not in db:
                db[self.KEY_USERS] = dict()

            if self.KEY_PRODUCTS not in db:
                db[self.KEY_PRODUCTS] = dict()

            if self.KEY_SHOPPING_CARTS not in db:
                db[self.KEY_SHOPPING_CARTS] = dict()

            if not db[self.KEY_USERS]:
                admin = User(
                    # Это uuid4 – уникальный идентификатор пользователя
                    id="29ae7ebf-4445-42f2-9548-a3a54f095220",
                    role=UserRole.ADMIN,
                    username="admin",
                    password="Admin_4321!",
                )
                db[self.KEY_USERS][admin.id] = admin

            has_key_products = bool(db[self.KEY_PRODUCTS])

        # В create_product и так открывается get_shelve
        if not has_key_products:
            self.create_product(
                name="Coca Cola 1л.",
                price_minor=8000,
                description="Газированный напиток",
            )
            self.create_product(
                name="Coca Cola 2л.",
                price_minor=13000,
                description="Газированный напиток",
            )
            self.create_product(
                name="Pepsi 1л.",
                price_minor=8000,
                description="Газированный напиток",
            )
            self.create_product(
                name="Сникерс",
                price_minor=4000,
                description="Шоколадный батончик",
            )

    def __init__(self):
        self._do_init_db_objects()

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

    def create_product(self, name: str, price_minor: int, description: str):
        with self.get_shelve() as db:
            obj = Product(
                id=str(uuid4()),
                name=name,
                price_minor=price_minor,
                description=description,
            )

            db[self.KEY_PRODUCTS][obj.id] = obj

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
    def add_product_in_shopping_cart(
        self, product: Product, shopping_cart: ShoppingCart
    ):
        shopping_cart.products.append(product)
        # TODO: ?
        self.create_shopping_cart(shopping_cart)

    # TODO: Для удаления продукта нужен только id
    def remove_product_from_shopping_cart(
        self, product: Product, shopping_cart: ShoppingCart
    ):
        shopping_cart.products.remove(product)
        # TODO: ?
        self.create_shopping_cart(shopping_cart)


db = DB()
