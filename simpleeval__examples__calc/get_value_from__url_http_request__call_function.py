#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

# pip install simpleeval
from simpleeval import SimpleEval


def get_from_url(value):
    rs = requests.get("https://httpbin.org/get", params={"value": value})
    return rs.json()["args"]["value"]


my_eval = SimpleEval()
my_eval.functions["get"] = get_from_url

print(my_eval.eval("get('123') + get('45')"))  # '12345'
print(my_eval.eval("int(get('123')) + int(get('45'))"))  # 168
