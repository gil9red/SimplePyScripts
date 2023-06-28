#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import time
import sys

import schedule

from vk_spam_wall import vk_auth, get_random_quotes, get_logger, run


logger = get_logger("vk_spam_wall_schedule")


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

    try:
        logger.debug("Задача запланирована на %s.", at)
        schedule.every().day.at(at).do(
            run,
            logger=logger,
            vk_session=vk_session,
            owner_id=owner_id,
            quote_count=quote_count,
        )

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logger.exception("Произошла ошибка:")
