#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/7320664/5909792
def xpath_get(mydict, path):
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            elem = elem.get(x)
    except:
        pass

    return elem


if __name__ == "__main__":
    data_1 = {"data": {"media": None}}

    data_2 = {
        "data": {
            "media": {
                "thumbnails": {
                    "original": {
                        "url": [
                            "http://...",
                            "https://...",
                        ]
                    }
                }
            }
        }
    }

    urls = xpath_get(data_1, "data/media/thumbnails/original/url")
    print(urls)  # None

    urls = xpath_get(data_2, "data/media/thumbnails/original/url")
    print(urls)  # ['http://...', 'https://...']
