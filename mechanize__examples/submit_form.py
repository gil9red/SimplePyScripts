#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

# pip install mechanize
import mechanize


br = mechanize.Browser()
br.open("https://httpbin.org/forms/post")

print(f"Title: {br.title()}")
print(f"URL: {br.geturl()}")

rs = br.response()

print("Headers:")
print(rs.info())
print()

print("Response body:")
print(rs.read())

print("\n" + "-" * 100 + "\n")

br.select_form(nr=0)  # First form
br["custname"] = "Customer"
br["custtel"] = "+79990001122"
br["custemail"] = "my@example.com"
br["size"] = ["medium"]  # radio
br["topping"] = ["bacon", "cheese"]  # checkbox
br["delivery"] = "11:15"
br["comments"] = "My comment!"

rs2 = br.submit()

print("Headers:")
print(rs2.info())
print()

rs2_body = rs2.read()
print("Response body:")
print(rs2_body)

rs2_json = json.loads(rs2_body)
print(rs2_json["form"])
# {'comments': 'My comment!', 'custemail': 'my@example.com', 'custname': 'Customer', 'custtel': '+79990001122',
# 'delivery': '11:15', 'size': 'medium', 'topping': ['bacon', 'cheese']}
