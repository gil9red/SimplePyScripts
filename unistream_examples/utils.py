#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import hmac
import hashlib
import logging

from datetime import datetime
from urllib.parse import urlsplit

from babel.dates import format_datetime


def get_today_RFC1123_date():
    now = datetime.utcnow()
    format = "EEE, dd LLL yyyy hh:mm:ss"
    return format_datetime(now, format, locale="en") + " GMT"


def hmac_sha256(key, msg):
    signature = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def get_authorization_header(application_id, secret, today_date, url, headers):
    logging.debug("Url:\n%s", url)

    url_parts = urlsplit(url)
    path_and_query = url_parts.path
    if url_parts.query:
        path_and_query += "?" + url_parts.query

    message = "GET\n\n" + today_date + "\n" + path_and_query.lower()

    # Конкатенация значений заголовков, соответствующих маске X-Unistream-*.
    # Заголовки сортируются по возрастанию по названию, приведенному к строчным буквам.
    # Значение каждого заголовка начинается с символа "\n"
    x_unistream_headers = [k for k in headers.keys() if "X-Unistream-" in k]
    if x_unistream_headers:
        x_unistream_headers.sort(key=str.lower)
        x_unistream_headers_value = [headers[k] for k in x_unistream_headers]
        message += "\n" + "\n".join(x_unistream_headers_value)

    secret = base64.b64decode(secret)
    signature = hmac_sha256(secret, message.encode())

    logging.debug("Message:\n%s", message)
    logging.debug("Signature:\n%s", signature)

    return f"UNIHMAC {application_id}:{signature}"
