#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re
import time

from html import unescape
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from config import DIR_DUMP


URL = "http://pravicon.com/s"
TIMEOUT_BETWEEN_REQUESTS = 0.010
DEBUG = False

SESSION = requests.session()
SESSION.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"


def secure_filename(text: str) -> str:
    return re.sub(r"\W", "_", text).strip("_")


def url_join(url_rel: str) -> str:
    return urljoin(URL, url_rel)


def parse(obj) -> BeautifulSoup:
    return BeautifulSoup(obj, "html.parser")


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/597dfd4ea77f0d57d2217ad02cde42cc23256c9b/html_parsing/random_quote_bash_im/bash_im.py#L29
def get_plaintext(element: Tag) -> str | None:
    if not element:
        return

    items = []
    for elem in element.descendants:
        if isinstance(elem, str):
            items.append(elem.strip())
        elif elem.name in ["br", "p"]:
            items.append("\n")
    return unescape("".join(items).strip())


def get(url: str, as_html=True) -> BeautifulSoup | requests.Response:
    while True:
        try:
            rs = SESSION.get(url)
            DEBUG and print(rs, rs.url)

            time.sleep(TIMEOUT_BETWEEN_REQUESTS)
            break

        except:
            time.sleep(10)

    if as_html:
        return parse(rs.content)

    return rs


def get_main_image_url(tag: Tag) -> str | None:
    """Картинка с страницы иконы. Расположение слева вверху."""

    el = tag.select_one("table td:nth-of-type(1) img[src]")
    if not el:
        return
    return url_join(el["src"])


def get_keywords(tag: Tag) -> str | None:
    """Ключевые слова с страницы иконы"""

    for p in tag.select("table td:nth-of-type(2) > p"):
        if "Ключевые слова:" in p.text:
            p.b.decompose()
            return p.get_text(strip=True)


def get_days_celebration(tag: Tag) -> str | None:
    """Дни празднования с страницы иконы"""

    el = tag.select_one("table td:nth-of-type(2) ul > li")
    if not el:
        return
    return el.get_text(strip=True, separator=" ")


def get_url_more_info(tag: Tag) -> str | None:
    """Возвращает ссылку на страницу с полным описанием.
    Такие ссылки присутствуют в "Описания иконы", "Богослужебные тексты"
    и в описании изображений икон
    """

    # Example:
    # <a href="/info-3677">
    #   <img src="/images/_web/ico_next.png" title="Читать далее..." alt="[далее]"
    #   width="50" height="13" border="0" align="absmiddle">
    # </a>
    more_info = tag.select_one('a:has(> img[alt="[далее]"])')
    if more_info:
        return url_join(more_info["href"])


def get_full_description(url: str, need_header=True) -> str:
    """Используется для извлечения описания с страниц полного описания.
    Такие страницы используются в "Описания иконы", "Богослужебные тексты"
    и в описании изображений икон
    """

    root = get(url)
    content_el = root.select_one("#content")

    for x in content_el.select("*"):
        if x.name in ["p", "script", "div", "table", "h1", "b"]:
            if x.name == "b" and "Описание:" in x.text:
                x.decompose()
                continue

            if x.name == "h1" and not need_header:
                x.decompose()
                continue

            x.decompose()

    return get_plaintext(content_el)


def get_description(tag: Tag) -> str | None:
    """Функция извлекается текст из "Описания иконы" с страницы иконы"""

    for spoiler in tag.select(".spoiler"):
        if "Описания иконы" in spoiler.b.text:
            url_more_info = get_url_more_info(spoiler)
            if url_more_info:
                return get_full_description(url_more_info)

            return get_plaintext(spoiler.select_one(".inner"))


def get_liturgical_texts(tag: Tag) -> str | None:
    """Функция извлекается текст из "Богослужебные тексты" с страницы иконы"""

    for spoiler in tag.select(".spoiler"):
        if "Богослужебные тексты" in spoiler.b.text:
            url_more_info = get_url_more_info(spoiler)
            if url_more_info:
                return get_full_description(url_more_info)

            return get_plaintext(spoiler.select_one(".inner"))


def get_image_description(tag: Tag) -> str | None:
    """Используется для извлечения описания у изображений икон"""

    for p in tag.select("p"):
        if "Описание:" in p.b.text:
            url_more_info = get_url_more_info(p)
            if url_more_info:
                return get_full_description(url_more_info, need_header=False)

            p.b.decompose()
            return get_plaintext(p)


def get_image_url(tag: Tag) -> str | None:
    """Используется для получения ссылки на полноразмерные изображения икон"""

    for p in tag.select("p"):
        if "Файл " in p.b.text:
            a = p.select_one('a[href *= "/download/i"]')
            if a:
                return url_join(a["href"])


def dump_icon(dir_dump: Path, url: str, title: str = None) -> None:
    dir_name = url.split("/")[-1] + "__" + secure_filename(title)
    dir_icon = dir_dump / dir_name
    dir_icon.mkdir(parents=True, exist_ok=True)

    # Файл, чье присутствие означает, что эта иконка полностью распарсена
    path_icon_finish = dir_icon / "__завершено__"
    if path_icon_finish.exists():
        return

    root = get(url)

    if not title:
        title = get_plaintext(root.select_one("#content > h1"))

    path_main_image = dir_icon / f"{secure_filename(title)}.jpg"
    path_info = dir_icon / "Информация.json"
    path_description = dir_icon / "Описания иконы.txt"
    path_liturgical_texts = dir_icon / "Богослужебные тексты.txt"

    url_main_image = get_main_image_url(root)
    if url_main_image:
        rs_img = get(url_main_image, as_html=False)
        path_main_image.write_bytes(rs_img.content)

    keywords = get_keywords(root)
    days_celebration = get_days_celebration(root)

    description = get_description(root)
    if description:
        path_description.write_text(description, "utf-8")

    liturgical_texts = get_liturgical_texts(root)
    if liturgical_texts and "В этом разделе записей пока нет" not in liturgical_texts:
        path_liturgical_texts.write_text(liturgical_texts, "utf-8")

    data_info = {
        "url": url,
        "title": title,
        "keywords": keywords,
        "days celebration": days_celebration,
    }
    json.dump(
        data_info, open(path_info, "w", encoding="utf-8"), ensure_ascii=False, indent=4
    )

    print(dir_icon)
    print("main image url:", url_main_image)
    print("keywords:", repr(keywords))
    print("days celebration:", repr(days_celebration))
    print("description:", repr(description))
    print("liturgical texts:", repr(liturgical_texts))

    # NOTE: Картинки оказались не нужны
    #
    # dir_icon_images = dir_icon / 'Изображения иконы'
    # dir_icon_images.mkdir(parents=True, exist_ok=True)
    #
    # root_images = get(url + '-photo')
    #
    # i = 1
    # for x in root_images.select('#images table tr > td > blockquote'):
    #     url_img = get_image_url(x)
    #     rs_img = get(url_img, as_html=False)
    #     description = get_image_description(x)
    #
    #     file_name_img = rs_img.url.split('/')[-1]
    #     print(f'#{i}.', url_img, file_name_img)
    #     print(repr(description))
    #
    #     path_img = dir_icon_images / file_name_img
    #     path_img.write_bytes(rs_img.content)
    #
    #     if description:
    #         path_description = dir_icon_images / (file_name_img + '.txt')
    #         path_description.write_text(description, 'utf-8')
    #
    #     print('\n' + '-' * 10 + '\n')
    #
    #     i += 1

    path_icon_finish.touch()


if __name__ == "__main__":
    root = get(URL)

    i = 0
    for a in root.select("table li > a[href]"):
        i += 1
        url_icon = url_join(a["href"])
        title = a.get_text(strip=True)

        print(f"#{i}. {url_icon} - {title!r}")
        dump_icon(DIR_DUMP, url_icon, title)

        print("\n" + "-" * 100 + "\n")
