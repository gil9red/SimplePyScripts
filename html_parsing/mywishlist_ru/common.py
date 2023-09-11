#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from dataclasses import dataclass, field
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_URL = "http://mywishlist.ru"


class VisibleModeEnum(Enum):
    PRIVATE = 0
    PUBLIC = 3
    FRIENDS = 2


class RatingEnum(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def get_logger(
    name: str,
    fmt: str = "[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    file: str | Path = "log.txt",
    encoding: str = "utf-8",
    log_stdout: bool = True,
    log_file: bool = True,
) -> "logging.Logger":
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt)

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10000000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


def parse(rs: requests.Response) -> BeautifulSoup:
    return BeautifulSoup(rs.content, "html.parser")


def do_get(url: str, *args, **kwargs) -> tuple[requests.Response, BeautifulSoup]:
    rs = session.get(url, *args, **kwargs)
    rs.raise_for_status()

    return rs, parse(rs)


def do_post(url: str, *args, **kwargs) -> tuple[requests.Response, BeautifulSoup]:
    rs = session.post(url, *args, **kwargs)
    rs.raise_for_status()

    return rs, parse(rs)


@dataclass
class Api:
    login: str
    password: str
    url_profile: str = None
    last_rs: requests.Response = field(init=False, repr=False, default=None)
    last_soup: BeautifulSoup = field(init=False, repr=False, default=None)
    log: logging.Logger = field(repr=False, default=None)

    def __post_init__(self):
        if not self.log:
            self.log = get_logger(
                name=__file__,
                fmt="%(message)s",
                log_file=False,
            )

    def _do_get(self, url: str, *args, **kwargs):
        self.log.debug(f"GET. url: {url}, args: {args}, kwargs: {kwargs}")
        self.last_rs, self.last_soup = do_get(url, *args, **kwargs)
        self.log.debug(f"GET. response url: {self.last_rs.url}")

    def _do_post(self, url: str, *args, **kwargs):
        self.log.debug(f"POST. url: {url}, args: {args}, kwargs: {kwargs}")
        self.last_rs, self.last_soup = do_post(url, *args, **kwargs)
        self.log.debug(f"POST. response url: {self.last_rs.url}")

    def auth(self):
        self.log.debug(f"Auth. {self.login}/{self.password}")

        url_get_login = f"{BASE_URL}/login"
        url_post_login = f"{BASE_URL}/login/login"

        self._do_get(url_get_login)

        params = {
            "login[login]": self.login,
            "login[password]": self.password,
        }

        self._do_post(url_post_login, data=params)
        if "/me/" not in self.last_rs.url:
            raise Exception(
                f"Не получилось авторизоваться! {self.last_rs} - {self.last_rs.url}"
            )

        self.url_profile = self.last_rs.url

    @classmethod
    def _get_authenticity_token(cls, soup: BeautifulSoup) -> str:
        authenticity_token_el = soup.select_one('[name="authenticity_token"]')
        return authenticity_token_el["value"]

    def add_wish(
        self,
        title: str,
        tags: list[str] = None,
        link: str = "",
        img_path: str = None,
        price_description: str = "",
        event: str = "",
        post_current: str = "",
        rating: RatingEnum = RatingEnum.MEDIUM,
        visible_mode: VisibleModeEnum = VisibleModeEnum.PUBLIC,
    ) -> int:
        self.log.info(f"Add wish. title: {title!r}")

        url_get_add_wish = f"{self.url_profile}/wish/add"
        self._do_get(url_get_add_wish)

        tags_value = ",".join(tags) if tags else ""
        params = {
            "authenticity_token": self._get_authenticity_token(self.last_soup),
            "wish[wish]": title,
            "wish[tags]": tags_value,
            "wish[link]": link,
            "wish[picture_delete]": "0",
            "wish[picture_url]": "",
            "wish[price]": price_description,
            "wish[event]": event,
            "wish[post_current]": post_current,
            "wish[rating]": rating.value,
            "wish[visible]": visible_mode.value,
            "wish[commentable]": "1",
        }

        files = []
        if img_path:
            files.append(
                ("wish[picture]", (img_path, open(img_path, "rb")))
            )

        url_post_add_wish = url_get_add_wish + "?autocomplete=false"
        self._do_post(
            url_post_add_wish,
            data=params,
            files=files
        )

        wish_el = self.last_soup.select_one('.pWishList .pWishData a[href*="/wish"]')
        if not wish_el:
            raise Exception("Не удалось найти желание!")

        return int(wish_el["href"].split("/")[-1])

    def set_wish_as_granted(self, wish_id: int, thanks: str = ""):
        self.log.info(f"Set wish as granted. wish_id: {wish_id}")

        url_get = f"{self.url_profile}/wish/check/{wish_id}"
        self._do_get(url_get)

        params = {
            "authenticity_token": self._get_authenticity_token(self.last_soup),
            "wish[realized]": "false",
            "wish[thanks]": thanks,
        }

        url_post = f"{self.url_profile}/wish/check_save/{wish_id}"
        self._do_post(
            url_post,
            data=params,
        )


if __name__ == "__main__":
    from datetime import datetime

    login = "9d57585a"
    password = "9d57585a-2643-4a2e-94da-b1068edfa087"

    api = Api(login, password)
    api.auth()

    wish_id = api.add_wish(
        title="Черника",
        tags=["еда", "eateateat", "черника", "ягоды", "тыгодки"],
        link="http://lesnayalavka.ru/product/svezhaya-chernika/",
        # img_path=r"E:\downloads\svezhuyu-cherniku-kupit-optom.jpg",
        event="хочу жрат",
        post_current="Хочу свеженькую тыгодку. Только, хуй, ее найдешь!",
        price_description="овердофига",
        rating=RatingEnum.HIGH,
    )
    print(f"Добавлено желание #{wish_id}")

    wish_id = api.add_wish(
        title=f"Желание #{int(datetime.now().timestamp())}",
        tags=["omnonom"],
        visible_mode=VisibleModeEnum.PRIVATE,
    )
    print(f"Добавлено желание #{wish_id}")

    wish_id = api.add_wish(
        title=f"Желание #{int(datetime.now().timestamp())}",
        img_path=r"..\..\pil_pillow__examples\blur\input.jpg",
        visible_mode=VisibleModeEnum.FRIENDS,
    )
    print(f"Добавлено желание #{wish_id}")

    api.set_wish_as_granted(wish_id, thanks="Благодарности моем коту!")
    print(f"Желание #{wish_id} исполнено!")
