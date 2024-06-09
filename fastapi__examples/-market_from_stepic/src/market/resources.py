#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import APIRouter, status, HTTPException
from fastapi.responses import HTMLResponse

from market.domains import Admin
from market.schemas import (
    GetArticlesModel,
    CreateArticleModel,
    LoginModel,
    GetArticleModel,
    ErrorModel,
)
from market import services
from market.repositories import ShelveArticlesRepository, MemoryUsersRepository


router = APIRouter()  # это роутер, он нужен для FastAPI, чтобы определять эндпоинты


@router.get("/")
def index():
    html_content = """
<div><a href="https://stepik.org/lesson/1186984/step/8?unit=1222202">Урок</a></div>
<br/>
<div><a href="/docs">/docs</a></div>
<div><a href="/redoc">/redoc</a></div>
    """
    return HTMLResponse(content=html_content)


@router.get("/articles", response_model=GetArticlesModel)
def get_articles() -> GetArticlesModel:
    # во всех представлениях всегда происходит одно и то же:
    # 1. получили данные
    # 2. вызвали сервисный метод и получили из него результат
    # 3. вернули результат клиенту в виде ответа
    articles = services.get_articles(articles_repository=ShelveArticlesRepository())
    return GetArticlesModel(
        items=[
            GetArticleModel(id=article.id, title=article.title, content=article.content)
            for article in articles
        ]
    )


@router.post(
    "/articles",
    response_model=GetArticleModel,
    # 201 статус код потому что мы создаем объект – стандарт HTTP
    status_code=status.HTTP_201_CREATED,
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
    responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def create_article(
    article: CreateArticleModel,
    # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    credentials: LoginModel,
):
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        users_repository=MemoryUsersRepository(),
    )

    # Это аутентификация
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )
    # а это авторизация
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
        )

    article = services.create_article(
        title=article.title,
        content=article.content,
        articles_repository=ShelveArticlesRepository(),
    )

    return GetArticleModel(id=article.id, title=article.title, content=article.content)
