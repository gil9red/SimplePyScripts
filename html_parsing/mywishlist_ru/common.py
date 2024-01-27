#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools
import logging
import io
import re
import sys
import time

from dataclasses import dataclass, field
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup, Tag

# pip install Pillow
from PIL import Image


BASE_URL = "http://mywishlist.ru"

PATTERN_GET_WISH_ID = re.compile(r"/wish/index/(\d+)")


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
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"


def parse(rs: requests.Response) -> BeautifulSoup:
    return BeautifulSoup(rs.content, "html.parser")


def attempts(
    max_number: int = 10,
    sleep: int = 60,
    ignored_exceptions: tuple[type(Exception)] = (RequestException,),
):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            number = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    number += 1
                    print(f"ERROR on {number}/{max_number}: {e}")

                    if number >= max_number or not isinstance(e, ignored_exceptions):
                        raise e

                    print(f"Sleep {sleep} seconds")
                    time.sleep(sleep)

        return wrapped

    return actual_decorator


@attempts()
def do_get(url: str, *args, **kwargs) -> tuple[requests.Response, BeautifulSoup]:
    rs = session.get(url, *args, **kwargs)
    rs.raise_for_status()

    return rs, parse(rs)


@attempts()
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

    @classmethod
    def _get_wish_list(cls, soup: BeautifulSoup) -> list[Tag]:
        return soup.select_one(".pWishList").find_all(
            name="a",
            attrs=dict(href=PATTERN_GET_WISH_ID),
        )

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
            if img_path.startswith("http"):
                try:
                    self._do_get(img_path)
                except requests.exceptions.SSLError as e:
                    self.log.warning(f'Ssl error "{e}" when loading "{img_path}", now trying without verification')
                    self._do_get(img_path, verify=False)

                buffer = io.BytesIO(self.last_rs.content)
            else:
                buffer = open(img_path, "rb")

            # Принудительно отправляем картинки в jpeg
            img = Image.open(buffer).convert("RGB")

            buffer = io.BytesIO()
            img.save(buffer, "jpeg")

            # После сохранения картинки нужно переместить внутренний указатель в начало
            buffer.seek(0)

            files.append(("wish[picture]", (img_path, buffer)))

        url_post_add_wish = url_get_add_wish + "?autocomplete=false"
        self._do_post(url_post_add_wish, data=params, files=files)

        wish_el_list = self._get_wish_list(self.last_soup)
        if not wish_el_list:
            raise Exception("Не удалось найти список желаний!")

        # Попробуем найти текущее желание по названию
        for wish_el in wish_el_list:
            if title in wish_el.text:
                wish_id = int(wish_el["href"].split("/")[-1])
                return wish_id

        raise Exception("Не удалось найти желание!")

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

        if not self.get_wish_is_granted(wish_id):
            raise Exception(f"Желание #{wish_id} не было отмечено как выполненное")

    def get_wish_is_granted(self, wish_id: int) -> bool:
        self.log.info(f"Get wish is granted. wish_id: {wish_id}")

        url_get = f"{self.url_profile}/wish/index/{wish_id}"
        self._do_get(url_get)

        # Если ссылки нет - желание исполнено
        return f"/wish/check/{wish_id}" not in self.last_rs.text

    def get_waiting_ids(self, get_all: bool = False) -> list[id]:
        self.log.info(f"Get waiting ids. get_all: {get_all}")

        url_get = f"{self.url_profile}/waiting"

        page = 1

        ids = []
        while True:
            params = {
                "view[sort]": "m",  # По времени
                "waiting_page": page,
            }
            self._do_get(url_get, params=params)

            # Поиск ид желаний по регулярке
            for a in self._get_wish_list(self.last_soup):
                m = PATTERN_GET_WISH_ID.search(a["href"])
                wish_id = int(m.group(1))
                if wish_id not in ids:
                    ids.append(wish_id)

            page += 1

            last_page_el = self.last_soup.select(
                ".pWishList > .pContainer .pNumbers a"
            )[-1]
            last_page = int(last_page_el.text)

            if not get_all or page > last_page:
                break

        return ids


if __name__ == "__main__":
    from datetime import datetime

    login = "9d57585a"
    password = "9d57585a-2643-4a2e-94da-b1068edfa087"

    api = Api(login, password)
    api.auth()

    ids = api.get_waiting_ids()
    print(f"Ids first page ({len(ids)}): {ids}")

    ids = api.get_waiting_ids(get_all=True)
    print(f"Ids all ({len(ids)}): {ids}")

    wish_id = api.add_wish(
        title="Черника",
        tags=["еда", "eateateat", "черника", "ягоды", "тыгодки"],
        link="http://lesnayalavka.ru/product/svezhaya-chernika/",
        img_path="https://calorizator.ru/sites/default/files/imagecache/product_512/product/bilberry.jpg",
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
    assert not api.get_wish_is_granted(wish_id)

    api.set_wish_as_granted(wish_id, thanks="Благодарности моем коту!")
    print(f"Желание #{wish_id} исполнено!")
    assert api.get_wish_is_granted(wish_id)
