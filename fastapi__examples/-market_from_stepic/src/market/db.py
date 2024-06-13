#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shelve
from uuid import uuid4

from market.config import DB_FILE_NAME
from market.models import User, Product, ShoppingCart, UserRole


class NotFoundException(Exception):
    pass


class DB:
    KEY_USERS: str = "users"
    KEY_PRODUCTS: str = "products"
    KEY_SHOPPING_CARTS: str = "shopping_carts"

    db_name: str = str(DB_FILE_NAME)

    def _generate_id(self) -> str:
        return str(uuid4())

    def _do_init_db_objects(self):
        with self.get_shelve() as db:
            if self.KEY_USERS not in db:
                db[self.KEY_USERS] = dict()

            if self.KEY_PRODUCTS not in db:
                db[self.KEY_PRODUCTS] = dict()

            if self.KEY_SHOPPING_CARTS not in db:
                db[self.KEY_SHOPPING_CARTS] = dict()

            has_key_users = bool(db[self.KEY_USERS])
            has_key_products = bool(db[self.KEY_PRODUCTS])

        # В create_user и так открывается get_shelve
        if not has_key_users:
            self.create_user(
                role=UserRole.ADMIN,
                username="admin",
                password="Admin_4321!",
                id="29ae7ebf-4445-42f2-9548-a3a54f095220",
            )

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

    def create_user(
        self,
        role: UserRole,
        username: str,
        password: str,
        id: str | None = None,
    ) -> User:
        with self.get_shelve() as db:
            obj = User(
                id=id if id else self._generate_id(),
                role=role,
                username=username,
                password=password,
            )
            db[self.KEY_USERS][obj.id] = obj
            return obj

    def create_product(self, name: str, price_minor: int, description: str) -> Product:
        with self.get_shelve() as db:
            obj = Product(
                id=self._generate_id(),
                name=name,
                price_minor=price_minor,
                description=description,
            )
            db[self.KEY_PRODUCTS][obj.id] = obj
            return obj

    def get_products(self) -> list[Product]:
        with self.get_shelve() as db:
            return list(db[self.KEY_PRODUCTS].values())

    def create_shopping_cart(self, product_ids: list[str]) -> ShoppingCart:
        with self.get_shelve() as db:
            obj = ShoppingCart(
                id=self._generate_id(),
                product_ids=product_ids,
            )
            db[self.KEY_SHOPPING_CARTS][obj.id] = obj
            return obj

    def update_shopping_cart(
        self,
        shopping_cart_id: str,
        product_ids: list[str],
    ):
        # TODO: дублирует
        with self.get_shelve() as db:
            shopping_cart: ShoppingCart | None = self.get_shopping_cart(shopping_cart_id)
            if not shopping_cart:
                raise NotFoundException(f"Shopping cart #{shopping_cart_id} not found!")

            shopping_cart.product_ids = product_ids

    def get_shopping_carts(self) -> list[ShoppingCart]:
        with self.get_shelve() as db:
            return list(db[self.KEY_SHOPPING_CARTS].values())

    def get_shopping_cart(self, id: str) -> ShoppingCart | None:
        with self.get_shelve() as db:
            return db[self.KEY_SHOPPING_CARTS].get(id)

    def add_product_in_shopping_cart(
        self,
        shopping_cart_id: str,
        product_id: str,
    ):
        # TODO: дублирует
        with self.get_shelve() as db:
            if product_id not in db[self.KEY_PRODUCTS]:
                raise NotFoundException(f"Product #{product_id} not found!")

            shopping_cart: ShoppingCart | None = self.get_shopping_cart(shopping_cart_id)
            if not shopping_cart:
                raise NotFoundException(f"Shopping cart #{shopping_cart_id} not found!")

        shopping_cart.product_ids.append(product_id)
        self.update_shopping_cart(shopping_cart_id, shopping_cart.product_ids)

    def remove_product_from_shopping_cart(
        self,
        shopping_cart_id: str,
        product_id: str,
    ):
        # TODO: дублирует
        with self.get_shelve() as db:
            if product_id not in db[self.KEY_PRODUCTS]:
                raise NotFoundException(f"Product #{product_id} not found!")

            shopping_cart: ShoppingCart | None = self.get_shopping_cart(shopping_cart_id)
            if not shopping_cart:
                raise NotFoundException(f"Shopping cart #{shopping_cart_id} not found!")

        shopping_cart.product_ids.remove(product_id)
        self.update_shopping_cart(shopping_cart_id, shopping_cart.product_ids)


db = DB()
