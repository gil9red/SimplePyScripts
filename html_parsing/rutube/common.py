#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys
from dataclasses import dataclass
from urllib.parse import ParseResult, urlparse, parse_qsl, urlencode

import requests


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/3377693e6b875394f0617a7c74fbd7fa834e1a0e/merge_url_params.py#L7-L17
def merge_url_params(url: str, params: dict) -> str:
    result: ParseResult = urlparse(url)

    current_params = dict(parse_qsl(result.query))
    merged_params = {**current_params, **params}

    new_query = urlencode(merged_params, doseq=True)
    return result._replace(query=new_query).geturl()


@dataclass
class Video:
    title: str
    url: str


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
