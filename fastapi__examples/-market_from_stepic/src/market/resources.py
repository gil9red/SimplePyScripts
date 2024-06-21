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
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

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

    raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.get("/users/me/")
def read_users_me(
    # TODO:
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
) -> models.User:
    return current_user


@router.get("/users")
def get_users(
    current_user: Annotated[models.Users, Depends(auth.get_current_user)],
) -> models.Users:
    # TODO:
    print(current_user)
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
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
) -> models.IdBasedObj:
    # TODO:
    print(current_user)

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


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/products",
    # 201 статус код потому что мы создаем объект – стандарт HTTP
    status_code=status.HTTP_201_CREATED,
    # TODO:
    # # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
    # responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def create_product(
    product: models.CreateProduct,
    # TODO:
    # # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    # credentials: LoginModel,
) -> models.IdBasedObj:
    # TODO:
    # current_user = services.login(
    #     username=credentials.username,
    #     password=credentials.password,
    #     users_repository=MemoryUsersRepository(),
    # )
    #
    # # Это аутентификация
    # if not current_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
    #     )
    # # а это авторизация
    # if not isinstance(current_user, Admin):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
    #     )

    return services.create_product(
        name=product.name,
        price_minor=product.price_minor,
        description=product.description,
    )


@router.get("/shopping-carts")
def get_shopping_carts() -> models.ShoppingCarts:
    return services.get_shopping_carts()


@router.get("/shopping-cart/{id}")
def get_shopping_cart(id: str) -> models.ShoppingCart:
    return services.get_shopping_cart(id)


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/shopping-carts",
    # 201 статус код потому что мы создаем объект – стандарт HTTP
    status_code=status.HTTP_201_CREATED,
    # TODO:
    # # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
    # responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def create_shopping_cart(
    shopping_cart: models.CreateShoppingCart,
    # TODO:
    # # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    # credentials: LoginModel,
) -> models.IdBasedObj:
    # TODO:
    # current_user = services.login(
    #     username=credentials.username,
    #     password=credentials.password,
    #     users_repository=MemoryUsersRepository(),
    # )
    #
    # # Это аутентификация
    # if not current_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
    #     )
    # # а это авторизация
    # if not isinstance(current_user, Admin):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
    #     )

    return services.create_shopping_cart(
        product_ids=shopping_cart.product_ids,
    )


# TODO:
# @router.post(
#     "/articles",
#     response_model=GetArticleModel,
#     # 201 статус код потому что мы создаем объект – стандарт HTTP
#     status_code=status.HTTP_201_CREATED,
#     # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
#     responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
# )
# def create_article(
#     article: CreateArticleModel,
#     # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
#     credentials: LoginModel,
# ):
#     current_user = services.login(
#         username=credentials.username,
#         password=credentials.password,
#         users_repository=MemoryUsersRepository(),
#     )
#
#     # Это аутентификация
#     if not current_user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
#         )
#     # а это авторизация
#     if not isinstance(current_user, Admin):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
#         )
#
#     article = services.create_article(
#         title=article.title,
#         content=article.content,
#         articles_repository=ShelveArticlesRepository(),
#     )
#
#     return GetArticleModel(id=article.id, title=article.title, content=article.content)
