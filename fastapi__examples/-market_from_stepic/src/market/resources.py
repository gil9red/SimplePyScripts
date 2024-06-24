#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from market import auth
from market import models
from market import services
from market.security import verify_password


router = APIRouter()


@router.post("/token")
def login_for_access_token(
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> models.LoginResponse:
    exception_400 = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username or password",
    )

    if not credentials.username or not credentials.password:
        raise exception_400

    user: models.UserInDb = services.get_user_by_username(credentials.username)
    if verify_password(credentials.password, user.hashed_password):
        # Generate a JWT token
        access_token = auth.create_access_token(
            token=auth.TokenPayload(user.id, user.role),
        )

        # Return the access token and user details
        return models.LoginResponse(
            token=access_token,
            user=models.User(
                id=user.id,
                username=user.username,
                role=user.role,
            ),
        )

    raise exception_400


@router.get("/users/me/")
def read_users_me(
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
) -> models.User:
    return current_user


@router.get("/users")
def get_users(
    _: Annotated[models.Users, Depends(auth.get_current_user_admin)],
) -> models.Users:
    return services.get_users()


@router.get("/user/{id}")
def get_user(id: str) -> models.User:
    return services.get_user(id)


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: models.CreateUser,
    _: Annotated[models.User, Depends(auth.get_current_user_admin)],
) -> models.IdBasedObj:
    return services.create_user(
        role=user.role,
        username=user.username,
        password=user.password,
    )


@router.get("/products")
def get_products() -> models.Products:
    return services.get_products()


@router.get("/product/{id}")
def get_product(id: str) -> models.Product:
    return services.get_product(id)


@router.patch("/product/{id}")
def update_product(
    id: str,
    other: models.UpdateProduct,
    current_user: Annotated[models.User, Depends(auth.get_current_user_manager_or_admin)],
) -> models.Product:
    if current_user.role == models.UserRoleEnum.MANAGER:
        # У менеджера нет прав на переименование продукта
        if other.name is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No rights to edit the name field",
            )

    services.update_product(
        id=id,
        name=other.name,
        price_minor=other.price_minor,
        description=other.description,
    )

    return services.get_product(id)


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: models.CreateProduct,
    _: Annotated[models.User, Depends(auth.get_current_user_admin)],
) -> models.IdBasedObj:
    return services.create_product(
        name=product.name,
        price_minor=product.price_minor,
        description=product.description,
    )


@router.get("/shopping-carts")
def get_shopping_carts(
    _: Annotated[models.User, Depends(auth.get_current_user_manager_or_admin)],
) -> models.ShoppingCarts:
    return services.get_shopping_carts()


@router.get("/shopping-cart/{id}")
def get_shopping_cart(id: str) -> models.ShoppingCart:
    return services.get_shopping_cart(id)


@router.post("/shopping-cart/{id}/products")
def add_product_in_shopping_cart(id: str, add_to: models.ProductsBasedObj) -> models.ShoppingCart:
    for product_id in add_to.product_ids:
        services.add_product_in_shopping_cart(
            shopping_cart_id=id, product_id=product_id
        )

    return services.get_shopping_cart(id)


@router.delete("/shopping-cart/{id}/products")
def remove_product_from_shopping_cart(id: str, remove_from: models.ProductsBasedObj) -> models.ShoppingCart:
    for product_id in remove_from.product_ids:
        services.remove_product_from_shopping_cart(
            shopping_cart_id=id, product_id=product_id
        )

    return services.get_shopping_cart(id)


@router.post(
    "/shopping-carts",
    status_code=status.HTTP_201_CREATED,
)
def create_shopping_cart(
    shopping_cart: models.CreateShoppingCart,
) -> models.IdBasedObj:
    return services.create_shopping_cart(
        product_ids=shopping_cart.product_ids,
    )


@router.get("/orders")
def get_orders(
    _: Annotated[models.User, Depends(auth.get_current_user_manager_or_admin)],
) -> models.Orders:
    return services.get_orders()


@router.get("/order/{id}")
def get_order(id: str) -> models.Order:
    return services.get_order(id)


@router.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order: models.CreateOrder,
) -> models.IdBasedObj:
    return services.create_order(
        email=order.email,
        shopping_cart_id=order.shopping_cart_id,
    )


# TODO:
# @router.patch("/orders/{id}")
# def update_order(
#     id: str,
#     other: models.Order, # TODO:
#     current_user: Annotated[models.User | None, Depends(auth.get_current_user_or_none)] = None,
# ) -> models.Order: # TODO:
#     order = services.get_order(id)
#
#     print(other, current_user)
#
#     return order

