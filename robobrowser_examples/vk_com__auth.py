#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from urllib.parse import urljoin

from robobrowser import RoboBrowser


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


browser = RoboBrowser(
    user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    parser="lxml",
)
browser.open("https://vk.com/login")

signup_form = browser.get_form()
signup_form["email"].value = LOGIN
signup_form["pass"].value = PASSWORD

# Submit the form
browser.submit_form(signup_form)

print(browser.response)

match = re.search(r"onLoginDone\('(.+)'\)", browser.response.text)
if match:
    url = urljoin(browser.url, match.group(1))
    browser.open(url)
    print(browser.response)

# If list is not empty, auth is successful
print(browser.select("#profile_edit_act"))
