#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import traceback

from urllib.parse import quote

import grab


if __name__ == "__main__":
    g = grab.Grab()

    tag_list = set()

    page = 1

    while True:
        try:
            url = f"http://ru.stackoverflow.com/tags?page={page}&tab=name"
            print(f"Go page (found tags: {len(tag_list)}): {url}")
            g.go(url)

            next_page = g.doc.select('//span[@class="page-numbers next"]')
            if not next_page.exists():
                break

            for a in g.doc.select('//a[@class="post-tag"]'):
                tag = a.text()

                url = f"http://ru.stackoverflow.com/tags/{quote(tag)}/info"
                print(f"  Go tag: {url}")

                tag_g = grab.Grab()
                tag_g.go(url)

                has_not_ref_guide = (
                    "Для этой метки до сих пор нет руководства по использованию."
                    in tag_g.response.body
                )
                has_not_description = (
                    "Для этой метки до сих пор нет описания." in tag_g.response.body
                )

                if has_not_ref_guide or has_not_description:
                    tag_info = (
                        tag,
                        has_not_ref_guide, has_not_description,
                        url
                    )
                    tag_list.add(tag_info)

                time.sleep(0.3)

            page += 1

            time.sleep(1)

        except Exception as e:
            # Сохраняем в переменную
            tb = traceback.format_exc()

            print(f"Error:\n{tb}")
            print("Wait 60 sec.")
            time.sleep(60)

    print(f"Tags: {len(tag_list)}.")
    for tag in tag_list:
        print(*tag)

    print(tag_list)
