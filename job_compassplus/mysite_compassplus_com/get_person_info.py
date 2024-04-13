#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from common import URL, do_get


@dataclass
class Person:
    name: str
    position: str
    department: str
    img_url: str
    location: str
    birthday: str

    def download_img(self) -> bytes:
        return do_get(self.img_url).content


def get_person_info(name: str, domain: str = "CP") -> Person | None:
    url = URL.format(fr"{domain}\{name}")

    rs = do_get(url)
    soup = BeautifulSoup(rs.content, "html.parser")

    img_el = soup.select_one("#ctl00_PictureUrlImage")
    if not img_el:  # Сайт не умеет показывать 404 при отсутствующем пользователе
        return

    default_value = "N/A"

    try:
        position = soup.select_one("#ProfileViewer_ValueTitle").get_text(strip=True)
        if not position:
            position = default_value
    except Exception:
        position = default_value

    try:
        department = soup.select_one("#ProfileViewer_ValueDepartment").get_text(strip=True)
        if not department:
            department = default_value
    except Exception:
        department = default_value

    try:
        location = soup.select_one('div[id *= "_ProfileViewer_SPS-Location"] > .ms-profile-detailsValue').get_text(strip=True)
        if not location:
            location = default_value
    except Exception:
        location = default_value

    try:
        birthday = soup.select_one('div[id *= "_ProfileViewer_SPS-Birthday"] > .ms-profile-detailsValue').get_text(strip=True)
        if not birthday:
            birthday = default_value
    except Exception:
        birthday = default_value

    return Person(
        name=name,
        position=position,
        department=department,
        img_url=urljoin(rs.url, img_el["src"]),
        location=location,
        birthday=birthday,
    )


if __name__ == "__main__":
    username = "ipetrash"

    info = get_person_info(username)
    print(info)
    # Person(name='ipetrash', position='Senior Software Engineer', department='TX SPD, Application Platforms Division', img_url='https://portal.compassplus.com/my/User%20Photos/Profile%20Pictures/ipetrash.jpg', location='Magnitogorsk', birthday='August 18')
