#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


# SOURCE: https://stackoverflow.com/a/1176023/5909792
def convert(text: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


if __name__ == "__main__":
    assert convert("CamelCase") == "camel_case"
    assert convert("CamelCamelCase") == "camel_camel_case"
    assert convert("Camel2Camel2Case") == "camel2_camel2_case"
    assert convert("getHTTPResponseCode") == "get_http_response_code"
    assert convert("get2HTTPResponseCode") == "get2_http_response_code"
    assert convert("HTTPResponseCode") == "http_response_code"
    assert convert("HTTPResponseCodeXYZ") == "http_response_code_xyz"
