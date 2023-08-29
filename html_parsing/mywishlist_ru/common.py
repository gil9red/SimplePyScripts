#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


BASE_URL = "http://mywishlist.ru"
URL_GET_LOGIN = f"{BASE_URL}/login"
URL_POST_LOGIN = f"{BASE_URL}/login/login"


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

    def auth(self) -> tuple[requests.Response, BeautifulSoup]:
        do_get(URL_GET_LOGIN)

        params = {
            "login[login]": self.login,
            "login[password]": self.password,
        }

        rs, root = do_post(URL_POST_LOGIN, data=params)

        if "/me/" not in rs.url:
            raise Exception("Не получилось авторизоваться!")

        return rs, root

    def add_wish(self, title: str, img_path: str = None) -> tuple[requests.Response, BeautifulSoup]:
        url_get_add_wish = f"{BASE_URL}/me/{self.login}/wish/add"
        url_post_add_wish = url_get_add_wish + "?autocomplete=false"

        do_get(url_get_add_wish)

        params = {
            "wish[wish]": title,
            "wish[tags]": "",
            "wish[link]": "",
            "wish[picture_delete]": "0",
            "wish[picture_url]": "",
            "wish[price]": "",
            "wish[event]": "",
            "wish[post_current]": "",
            "wish[rating]": "2",
            "wish[visible]": "0",
            "wish[commentable]": "1",
        }

        files = []
        if img_path:
            files.append(
                ("wish[picture]", (img_path, open(img_path, "rb")))
            )

        return do_post(url_post_add_wish, data=params, files=files)


if __name__ == "__main__":
    from datetime import datetime

    login = "9d57585a"
    password = "9d57585a-2643-4a2e-94da-b1068edfa087"

    api = Api(login, password)
    api.auth()
    api.add_wish(
        title=f"Желание #{int(datetime.now().timestamp())}",
    )
    api.add_wish(
        title=f"Желание #{int(datetime.now().timestamp())}",
        img_path=r"..\..\pil_pillow__examples\blur\input.jpg",
    )
