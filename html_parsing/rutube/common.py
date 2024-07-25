#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import logging
import re
import sys

from dataclasses import dataclass
from typing import Any
from urllib.parse import ParseResult, urlparse, parse_qsl, urlencode

import requests


@dataclass
class Video:
    title: str
    url: str


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/3377693e6b875394f0617a7c74fbd7fa834e1a0e/merge_url_params.py#L7-L17
def merge_url_params(url: str, params: dict) -> str:
    result: ParseResult = urlparse(url)

    current_params = dict(parse_qsl(result.query))
    merged_params = {**current_params, **params}

    new_query = urlencode(merged_params, doseq=True)
    return result._replace(query=new_query).geturl()


def get_redux_state(html: str) -> dict[str, Any]:
    # Первая порция данных находится в странице как объект js
    m = re.search(r"window\.reduxState\s*=\s*(\{.+});", html)
    if not m:
        raise Exception('Не найдено "window.reduxState"!')

    # Подмена всяких "\x3d" на конкретные символы
    js_text = re.sub(
        r"\\x([0-9a-fA-F]{2})",
        lambda x: chr(int(x.group(1), 16)),
        m.group(1),
    )

    data: dict[str, Any] = json.loads(js_text)
    logger.debug(f"data: {data}")

    return data


default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)
logger = logging.getLogger("rutube-parser")
logger.setLevel(logging.WARNING)
logger.addHandler(default_handler)

session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/127.0"
