#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from uuid import uuid4

from market.domains import Article, User
from market.repositories import ArticlesRepository, UsersRepository


def get_articles(articles_repository: ArticlesRepository) -> list[Article]:
    return articles_repository.get_articles()


def create_article(
    title: str, content: str, articles_repository: ArticlesRepository
) -> Article:
    article = Article(id=str(uuid4()), title=title, content=content)
    articles_repository.create_article(article=article)
    return article


def login(
    username: str, password: str, users_repository: UsersRepository
) -> User | None:
    users = users_repository.get_users(username=username, password=password)
    if users:
        return users[0]
