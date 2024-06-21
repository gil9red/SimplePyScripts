#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools
import threading
import shelve

from pathlib import Path
from typing import Any
from uuid import uuid4

from market import models
from market.config import DB_FILE_NAME
from market.security import get_password_hash


class NotFoundException(Exception):
    pass


class DB:
    KEY_USERS: str = "users"
    KEY_PRODUCTS: str = "products"
    KEY_SHOPPING_CARTS: str = "shopping_carts"

    _mutex = threading.RLock()

    def session(*decorator_args, **decorator_kwargs):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                with self._mutex:
                    has_db: bool = self.db is not None
                    try:
                        if not has_db:
                            self.db = shelve.open(self.file_name, writeback=True)
                        return func(self, *args, **kwargs)
                    finally:
                        if not has_db and self.db is not None:
                            self.db.close()
                            self.db = None
            return wrapped
        return actual_decorator

    def lock(*decorator_args, **decorator_kwargs):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                with self._mutex:
                    return func(self, *args, **kwargs)
            return wrapped
        return actual_decorator

    @session()
    def get_value(self, name: str, default: Any = None) -> Any:
        if not name:
            return dict(self.db)

        if name not in self.db:
            return default
        return self.db.get(name)

    @session()
    def set_value(self, name: str, value: Any):
        self.db[name] = value

    def __init__(self, file_name: Path | str = DB_FILE_NAME):
        self.file_name: str = str(file_name)
        self.db: shelve.Shelf | None = None

        self._do_init_db_objects()

    def _generate_id(self) -> str:
        return str(uuid4())

    @lock()
    def _do_init_db_objects(self):
        if self.KEY_USERS not in self.get_value(""):
            self.set_value(self.KEY_USERS, dict())

        if self.KEY_PRODUCTS not in self.get_value(""):
            self.set_value(self.KEY_PRODUCTS, dict())

        if self.KEY_SHOPPING_CARTS not in self.get_value(""):
            self.set_value(self.KEY_SHOPPING_CARTS, dict())

        if not self.get_value(self.KEY_USERS):
            self.create_user(
                role=models.UserRoleEnum.ADMIN,
                username="admin",
                password="Admin_4321!",
                id="29ae7ebf-4445-42f2-9548-a3a54f095220",
            )

        if not self.get_value(self.KEY_PRODUCTS):
            self.create_product(
                name="Coca Cola 1л.",
                price_minor=8000,
                description="Газированный напиток",
            )
            self.create_product(
                name="Coca Cola 2л.",
                price_minor=13500,
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

    @lock()
    def get_users(
        self,
        username: str | None = None,
    ) -> list[models.UserInDb]:
        """
        :param username: фильтр по логину

        :return: отфильтрованные пользователи
        """

        filtered_users = []  # Тут собираются отфильтрованные пользователи

        # Перебираем всех пользователей и оставляем только тех, кто прошел фильтры
        for user in self.get_value(self.KEY_USERS).values():
            if username is not None and user.username != username:
                continue
            filtered_users.append(user)

        return filtered_users

    @lock()
    def get_user(self, id: str, check_exists: bool = False) -> models.UserInDb | None:
        obj = self.get_value(self.KEY_USERS).get(id)
        if obj is None and check_exists:
            raise NotFoundException(f"User #{id} not found!")
        return obj

    @lock()
    def get_user_by_username(
        self,
        username: str,
        check_exists: bool = False,
    ) -> models.UserInDb | None:
        users = self.get_users(username=username)
        if users:
            return users[0]

        if check_exists:
            raise NotFoundException(f'User "{username}" not found!')

    @lock()
    def create_user(
        self,
        role: models.UserRoleEnum,
        username: str,
        password: str,
        id: str | None = None,
    ) -> models.UserInDb:
        # TODO: Проверка уникальности username
        obj = models.UserInDb(
            id=id if id else self._generate_id(),
            role=role,
            username=username,
            hashed_password=get_password_hash(password),
        )
        users = self.get_value(self.KEY_USERS)
        users[obj.id] = obj
        self.set_value(self.KEY_USERS, users)
        return obj

    @lock()
    def create_product(
        self, name: str, price_minor: int, description: str
    ) -> models.Product:
        obj = models.Product(
            id=self._generate_id(),
            name=name,
            price_minor=price_minor,
            description=description,
        )
        products = self.get_value(self.KEY_PRODUCTS)
        products[obj.id] = obj
        self.set_value(self.KEY_PRODUCTS, products)
        return obj

    @lock()
    def get_products(self) -> list[models.Product]:
        return list(self.get_value(self.KEY_PRODUCTS).values())

    @lock()
    def get_product(self, id: str, check_exists: bool = False) -> models.Product | None:
        obj = self.get_value(self.KEY_PRODUCTS).get(id)
        if obj is None and check_exists:
            raise NotFoundException(f"Product #{id} not found!")
        return obj

    @lock()
    def create_shopping_cart(self, product_ids: list[str]) -> models.ShoppingCart:
        obj = models.ShoppingCart(
            id=self._generate_id(),
            product_ids=product_ids,
        )
        shopping_carts = self.get_value(self.KEY_SHOPPING_CARTS)
        shopping_carts[obj.id] = obj
        self.set_value(self.KEY_SHOPPING_CARTS, shopping_carts)
        return obj

    @lock()
    def update_shopping_cart(
        self,
        shopping_cart_id: str,
        product_ids: list[str],
    ):
        shopping_cart: models.ShoppingCart | None = self.get_shopping_cart(
            shopping_cart_id, check_exists=True
        )
        shopping_cart.product_ids = product_ids

        shopping_carts = self.get_value(self.KEY_SHOPPING_CARTS)
        self.set_value(self.KEY_SHOPPING_CARTS, shopping_carts)

    @lock()
    def get_shopping_carts(self) -> list[models.ShoppingCart]:
        return list(self.get_value(self.KEY_SHOPPING_CARTS).values())

    @lock()
    def get_shopping_cart(
        self,
        id: str,
        check_exists: bool = False,
    ) -> models.ShoppingCart | None:
        obj = self.get_value(self.KEY_SHOPPING_CARTS).get(id)
        if obj is None and check_exists:
            raise NotFoundException(f"Shopping cart #{id} not found!")
        return obj

    @lock()
    def add_product_in_shopping_cart(
        self,
        shopping_cart_id: str,
        product_id: str,
    ):
        # Проверка наличия
        self.get_product(product_id, check_exists=True)

        shopping_cart: models.ShoppingCart | None = self.get_shopping_cart(
            shopping_cart_id, check_exists=True
        )

        shopping_cart.product_ids.append(product_id)
        self.update_shopping_cart(shopping_cart_id, shopping_cart.product_ids)

    @lock()
    def remove_product_from_shopping_cart(
        self,
        shopping_cart_id: str,
        product_id: str,
    ):
        # Проверка наличия
        self.get_product(product_id, check_exists=True)

        shopping_cart: models.ShoppingCart | None = self.get_shopping_cart(
            shopping_cart_id, check_exists=True
        )
        shopping_cart.product_ids.remove(product_id)
        self.update_shopping_cart(shopping_cart_id, shopping_cart.product_ids)


db = DB()


if __name__ == "__main__":
    # TODO: В тесты
    from market.config import DB_TEST_FILE_NAME
    db_test = DB(file_name=DB_TEST_FILE_NAME)

    value = db_test.get_value("counter", default=1)
    print(f"Counter: {value}")

    def inc_counter():
        value = db_test.get_value("counter", default=1)
        db_test.set_value("counter", value + 1)

    inc_counter()

    # TODO: не рабочий вариант, нужно использовать методы самого DB
    # current_value = db_test.get_value("counter", default=1)
    #
    # max_workers = 5
    # number = 50
    # expected_value = current_value + number
    #
    # import concurrent.futures
    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     futures = [executor.submit(inc_counter) for _ in range(number)]
    #     concurrent.futures.wait(futures)
    #
    # print(expected_value, db_test.get_value("counter", default=1))
