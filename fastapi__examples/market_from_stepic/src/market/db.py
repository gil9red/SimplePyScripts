#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools
import threading
import shelve

from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from market import models
from market.config import DB_FILE_NAME
from market.security import get_password_hash


class DbException(Exception):
    pass


class NotFoundException(DbException):
    pass


class InvalidException(DbException):
    pass


class InvalidOrderStatusException(InvalidException):
    def __init__(self, prev_status: models.StatusOrderEnum, new_status: models.StatusOrderEnum) -> None:
        super().__init__(f"Unable to change order status {prev_status.value!r} to {new_status.value!r}")


class DB:
    KEY_USERS: str = "users"
    KEY_PRODUCTS: str = "products"
    KEY_SHOPPING_CARTS: str = "shopping_carts"
    KEY_ORDERS: str = "orders"
    KEY_INDEXES: str = "[indexes]"

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
    def set_value(self, name: str, value: Any) -> None:
        self.db[name] = value

    def __init__(self, file_name: Path | str = DB_FILE_NAME) -> None:
        self.file_name: str = str(file_name)
        self.db: shelve.Shelf | None = None

        self._do_init_db_objects()

    def _generate_id(self) -> str:
        return str(uuid4())

    @lock()
    def rebuild_indexes(self, clear: bool = True) -> None:
        indexes: dict[str, dict[str, str]] = self.get_value(self.KEY_INDEXES, default=dict())

        if self.KEY_USERS not in indexes:
            indexes[self.KEY_USERS] = dict()

        if self.KEY_PRODUCTS not in indexes:
            indexes[self.KEY_PRODUCTS] = dict()

        if clear:
            indexes.clear()

            indexes[self.KEY_USERS] = {obj.username: obj.id for obj in self.get_users()}
            indexes[self.KEY_PRODUCTS] = {obj.name: obj.id for obj in self.get_products()}

        self.set_value(self.KEY_INDEXES, indexes)

    @lock()
    def add_index(self, table: str, key: str, id: str) -> None:
        indexes: dict[str, dict[str, str]] = self.get_value(self.KEY_INDEXES)
        indexes[table][key] = id

        self.set_value(self.KEY_INDEXES, indexes)

    @lock()
    def remove_index(self, table: str, key: str) -> None:
        indexes: dict[str, dict[str, str]] = self.get_value(self.KEY_INDEXES)
        indexes[table].pop(key)

        self.set_value(self.KEY_INDEXES, indexes)

    @lock()
    def get_id_from_index(self, table: str, key: str) -> str | None:
        indexes: dict[str, dict[str, str]] = self.get_value(self.KEY_INDEXES)
        return indexes[table].get(key)

    @lock()
    def _do_init_db_objects(self) -> None:
        self.rebuild_indexes(clear=False)

        if self.KEY_USERS not in self.get_value(""):
            self.set_value(self.KEY_USERS, dict())

        if self.KEY_PRODUCTS not in self.get_value(""):
            self.set_value(self.KEY_PRODUCTS, dict())

        if self.KEY_SHOPPING_CARTS not in self.get_value(""):
            self.set_value(self.KEY_SHOPPING_CARTS, dict())

        if self.KEY_ORDERS not in self.get_value(""):
            self.set_value(self.KEY_ORDERS, dict())

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
        obj_id: str | None = self.get_id_from_index(self.KEY_USERS, username)
        return self.get_user(
            id=obj_id,
            check_exists=check_exists,
        )

    @lock()
    def create_user(
        self,
        role: models.UserRoleEnum,
        username: str,
        password: str,
        id: str | None = None,
    ) -> models.UserInDb:
        obj_id: str | None = self.get_id_from_index(self.KEY_USERS, username)
        if obj_id:
            raise DbException(f"Cannot create user {username!r} - this nickname is taken")

        obj = models.UserInDb(
            id=id if id else self._generate_id(),
            role=role,
            username=username,
            hashed_password=get_password_hash(password),
        )
        self.add_index(self.KEY_USERS, username, obj.id)

        users = self.get_value(self.KEY_USERS)
        users[obj.id] = obj
        self.set_value(self.KEY_USERS, users)
        return obj

    @lock()
    def create_product(
        self,
        name: str,
        price_minor: int,
        description: str,
    ) -> models.Product:
        obj_id: str | None = self.get_id_from_index(self.KEY_PRODUCTS, name)
        if obj_id:
            raise DbException(f"Cannot create product {name!r} - this name is taken")

        obj = models.Product(
            id=self._generate_id(),
            name=name,
            price_minor=price_minor,
            description=description,
        )
        self.add_index(self.KEY_PRODUCTS, name, obj.id)

        products = self.get_value(self.KEY_PRODUCTS)
        products[obj.id] = obj
        self.set_value(self.KEY_PRODUCTS, products)
        return obj

    @lock()
    def update_product(
        self,
        id: str,
        name: str | None = None,
        price_minor: int | None = None,
        description: str | None = None,
    ) -> None:
        product = self.get_product(id, check_exists=True)

        if name is not None:
            product.name = name

        if price_minor is not None:
            product.price_minor = price_minor

        if description is not None:
            product.description = description

        products = self.get_value(self.KEY_PRODUCTS)
        products[id] = product

        self.set_value(self.KEY_PRODUCTS, products)

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
    def delete_shopping_cart(self, shopping_cart_id: str) -> None:
        # Проверка наличия
        self.get_shopping_cart(shopping_cart_id, check_exists=True)

        shopping_carts: dict = self.get_value(self.KEY_SHOPPING_CARTS)
        shopping_carts.pop(shopping_cart_id)

        self.set_value(self.KEY_SHOPPING_CARTS, shopping_carts)

    @lock()
    def update_shopping_cart(
        self,
        shopping_cart_id: str,
        product_ids: list[str],
    ) -> None:
        shopping_cart: models.ShoppingCart = self.get_shopping_cart(
            shopping_cart_id, check_exists=True
        )
        shopping_cart.product_ids = product_ids

        shopping_carts = self.get_value(self.KEY_SHOPPING_CARTS)
        shopping_carts[shopping_cart_id] = shopping_cart

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
    ) -> None:
        shopping_cart: models.ShoppingCart = self.get_shopping_cart(
            shopping_cart_id, check_exists=True
        )

        # Проверка наличия
        self.get_product(product_id, check_exists=True)

        shopping_cart.product_ids.append(product_id)
        self.update_shopping_cart(shopping_cart_id, shopping_cart.product_ids)

    @lock()
    def remove_product_from_shopping_cart(
        self,
        shopping_cart_id: str,
        product_id: str,
    ) -> None:
        shopping_cart: models.ShoppingCart = self.get_shopping_cart(
            shopping_cart_id, check_exists=True
        )

        # Проверка наличия
        self.get_product(product_id, check_exists=True)

        if product_id in shopping_cart.product_ids:
            shopping_cart.product_ids.remove(product_id)

        self.update_shopping_cart(shopping_cart_id, shopping_cart.product_ids)

    @lock()
    def create_order(
        self,
        email: str,
        shopping_cart_id: str,
    ) -> models.Order:
        # Проверка наличия
        self.get_shopping_cart(shopping_cart_id, check_exists=True)

        obj = models.Order(
            id=self._generate_id(),
            email=email,
            shopping_cart_id=shopping_cart_id,
        )
        orders = self.get_value(self.KEY_ORDERS)
        orders[obj.id] = obj
        self.set_value(self.KEY_ORDERS, orders)
        return obj

    @lock()
    def update_order(
        self,
        id: str,
        email: str | None = None,
        shopping_cart_id: str | None = None,
        status: models.StatusOrderEnum | None = None,
        cancel_reason: str | None = None,
    ):
        order = self.get_order(id, check_exists=True)

        complete_statuses = (models.StatusOrderEnum.FINISHED, models.StatusOrderEnum.CANCELED)
        if order.status in complete_statuses:
            raise DbException(f"It is forbidden to update an order with status {order.status.value!r}")

        if email is not None:
            order.email = email

        if shopping_cart_id is not None:
            # Проверка наличия
            self.get_shopping_cart(shopping_cart_id, check_exists=True)

            order.shopping_cart_id = shopping_cart_id

        if status is not None and status != order.status:
            invalid_status_exception = InvalidOrderStatusException(order.status, status)

            match order.status:
                case models.StatusOrderEnum.CREATED:
                    pass
                case models.StatusOrderEnum.IN_PROCESSED:
                    # Если текущий статус "в процессе", то следующий может быть или отмена, или завершение
                    if status not in complete_statuses:
                        raise invalid_status_exception
                case models.StatusOrderEnum.CANCELED:
                    raise invalid_status_exception
                case models.StatusOrderEnum.FINISHED:
                    raise invalid_status_exception
                case _:
                    raise InvalidException(f"Unsupported status {status.value!r}!")

            order.status = status

            if status in complete_statuses:
                order.closed_date = datetime.now()

        if cancel_reason is not None:
            order.cancel_reason = cancel_reason

        orders = self.get_value(self.KEY_ORDERS)
        orders[id] = order

        self.set_value(self.KEY_ORDERS, orders)

    @lock()
    def get_orders(self) -> list[models.Order]:
        return list(self.get_value(self.KEY_ORDERS).values())

    @lock()
    def get_order(
        self,
        id: str,
        check_exists: bool = False,
    ) -> models.Order | None:
        obj = self.get_value(self.KEY_ORDERS).get(id)
        if obj is None and check_exists:
            raise NotFoundException(f"Order #{id} not found!")
        return obj


db = DB()


if __name__ == "__main__":
    # db.rebuild_indexes()
    print(db.get_value(""))

    # # TODO: В тесты
    # from market.config import DB_TEST_FILE_NAME
    # db_test = DB(file_name=DB_TEST_FILE_NAME)
    #
    # value = db_test.get_value("counter", default=1)
    # print(f"Counter: {value}")
    #
    # def inc_counter():
    #     value = db_test.get_value("counter", default=1)
    #     db_test.set_value("counter", value + 1)
    #
    # inc_counter()

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
