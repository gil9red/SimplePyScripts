#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Download tags with description and save in file as JSON.

"""


import itertools
import time
import traceback

import requests
from bs4 import BeautifulSoup


def get_all_tags(
    need_pages=None,
    need_tags=None,
    on_exception_stop=False,
    repeat_request_tag_on_error=True,
) -> dict:
    """
    Функция парсит страницу тегов/меток и возвращает их.

    :param need_pages: Т.к. теги будут в порядке убывания популярности, то теги на первых десятках страниц будут
    гарантировано заполнены, из-за их популярности, остальные может не иметь смысла скачивать
    Пример получения первых 20 страниц: NEED_PAGES = 20
    :param need_tags: ограничение на количество тегов, что нужно загрузить
    :param on_exception_stop: если True и при парсинге возникнет исключение, парсер будет остановлен
    :param repeat_request_tag_on_error: если True, запрос парсинга тега будет повторяться пока не будет удачен
    :return: dict
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    tags = dict()

    for page in itertools.count(start=1):
        print("page:", page)

        try:
            rs = requests.get(
                f"http://ru.stackoverflow.com/tags?page={page}&tab=popular",
                headers=headers,
            )
            root = BeautifulSoup(rs.content, "html.parser")

            for tag in [a.text.strip() for a in root.select(".tag-cell > a")]:
                print(f'  tag: "{tag}"')
                url_info = f"http://ru.stackoverflow.com/tags/{tag}/info"

                while True:
                    try:
                        rs = requests.get(url_info, headers=headers)
                        root = BeautifulSoup(rs.content, "html.parser")

                        # TODO: Ignore tags without description
                        tag_text = root.select_one(".post-text")
                        if tag_text:
                            tags[tag] = {
                                "url_info": url_info,
                                "description": tag_text.text.strip(),
                            }

                            # TODO: удалить текст
                            # Для этой метки до сих пор нет описания.
                            # Описание помогает новичкам глубже понять тематику метки, содержит обзор темы, которую
                            # представляет метка, а также инструкции по её использованию.
                            # Все зарегистированные пользователи могут предлагать новые описания меток.
                            # (Обратите внимание: если у вас меньше 20000 баллов репутации, то перед публикацией ваши
                            # изменения в описании метки должны будут пройти проверку).

                            # TODO: удалить лишние пробелы, \n и \t
                            # description = re.sub(' {2,}', ' ', description)
                            # description = re.sub('\n{2,}', '\n', description)
                            # description = re.sub('\t{2,}', '\t', description)

                            if need_tags and len(tags) == need_tags:
                                return tags

                        # Нам не нужно ДОСить сайт
                        time.sleep(2)
                        break

                    except Exception as e:
                        print(f"ERROR: {e}\n\n{traceback.format_exc()}")

                        if not repeat_request_tag_on_error:
                            break

        except Exception as e:
            print(f"ERROR: {e}\n\n{traceback.format_exc()}")

            if on_exception_stop:
                break

        print()

        if page == need_pages:
            break

    return tags


if __name__ == "__main__":
    # # Parse all pages:
    # tags = get_all_tags()

    # # Parse 2 tags
    # tags = get_all_tags(need_tags=2)
    # print(tags)

    tags = get_all_tags(need_pages=20)

    import json

    json.dump(tags, open("tags.json", "w", encoding="utf-8"), ensure_ascii=False)
