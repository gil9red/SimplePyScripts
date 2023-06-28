#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import json
import time
import sys

from pathlib import Path

import vk_api

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_common import get_logger

# Для импортирования bash_im.py
sys.path.append(str(ROOT_DIR.parent / "html_parsing" / "random_quote_bash_im"))
from bash_im import get_random_quotes


def vk_auth(login: str, password: str) -> vk_api.VkApi:
    vk = vk_api.VkApi(login, password)

    try:
        logger.debug("Авторизуюсь в vk.")
        vk.auth()
    except Exception as e:
        logger.exception("При авторизации произошла ошибка:")
        sys.exit()

    logger.debug("Успешная авторизация.")

    return vk


def wall_post(logger, vk_session: vk_api.VkApi, owner_id: int, quote_href: str):
    logger.debug("Размещаю сообщение на стену.")

    # Добавление сообщения на стену пользователя (owner_id это id пользователя)
    # Если не указывать owner_id, сообщения себе на стену поместится
    rs = vk_session.method(
        "wall.post",
        {
            "owner_id": owner_id,
            "attachments": quote_href,
        },
    )

    logger.debug("post_id: %s, quote href: %s.", rs["post_id"], quote_href)


def run(logger, vk_session: vk_api.VkApi, owner_id: int, quote_count: int):
    # Начинаем постить на стену
    for quote in get_random_quotes()[:quote_count]:
        wall_post(logger, vk_session, owner_id, quote.url)
        time.sleep(0.4)


logger = get_logger("vk_spam_wall", DIR / "log.txt")


if __name__ == "__main__":
    logger.debug("Начало работы.")
    logger.debug("Читаю файл конфига.")
    config = json.load(open("config.json"))

    # Логин, пароль к аккаунту и id человека, на стену которого будем постить сообщения
    login = config["login"]
    password = config["password"]
    to_owner_id = config["to_owner_id"]
    at = config["at"]
    quote_count = config["quote_count"]

    logger.debug("Закончено чтение файла конфига. Конфиг: %s.", config)

    if not login or not password:
        logger.error("Логин/пароль не указаны.")
        sys.exit()

    # Авторизуемся
    vk_session = vk_auth(login, password)

    # Если определен, то узнаем id пользователя которого будем спамить, иначе шлем самим себе
    if to_owner_id:
        rs = vk_session.method("users.get", dict(user_ids=to_owner_id))[0]
        owner_id = int(rs["id"])
    else:
        owner_id = None

    at_time = DT.datetime.strptime(at, "%H:%M").time()

    while True:
        # Ждем наступления времени, указанного в at
        while True:
            # Убираем микросекунды, иначе совпадения вряд ли дождемся в этой жизни
            now = DT.datetime.today().time()
            now = now.replace(microsecond=0)
            if now == at_time:
                break

            time.sleep(0.3)

        try:
            run(logger, vk_session, owner_id, quote_count)

        except Exception as e:
            logger.exception("Произошла ошибка:")
