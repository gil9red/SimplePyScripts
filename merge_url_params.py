#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import ParseResult, urlparse, urlencode, parse_qsl


def merge_url_params(url: str, params: dict) -> str:
    result: ParseResult = urlparse(url)

    current_params = dict(parse_qsl(result.query))
    merged_params = {**current_params, **params}

    new_query = urlencode(merged_params, doseq=True)
    return result._replace(query=new_query).geturl()


if __name__ == "__main__":
    url = "https://examples.com/jobs/search?keywords=engineer"
    new_params = {"location": "United States", "keywords": True, "items": [1, 2, 3]}

    assert (
        merge_url_params(url, new_params)
        == "https://examples.com/jobs/search?keywords=True&location=United+States&items=1&items=2&items=3"
    )

    url = "https://examples.com/jobs/search"
    assert (
        merge_url_params(url, new_params)
        == "https://examples.com/jobs/search?location=United+States&keywords=True&items=1&items=2&items=3"
    )
