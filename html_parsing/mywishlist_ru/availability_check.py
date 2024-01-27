#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from requests.exceptions import ConnectionError
from common import BASE_URL, get_logger, session


log = get_logger(
    __file__,
    fmt="[%(asctime)s] %(message)s",
    log_file=False,
)

log.info(f"Проверка сайта {BASE_URL}")
log.info("")

availability = None
while True:
    try:
        session.get(BASE_URL)

        if availability is None or not availability:
            log.info("Сайт доступен")
            availability = True

    except ConnectionError:
        if availability is None or availability:
            log.info("Сайт не доступен")
            availability = False

    time.sleep(60)
