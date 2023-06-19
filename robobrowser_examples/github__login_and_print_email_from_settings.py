#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from robobrowser import RoboBrowser


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


browser = RoboBrowser(
    user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
    parser="lxml",
)
browser.open("https://github.com/login")

signup_form = browser.get_form()
signup_form["login"].value = LOGIN
signup_form["password"].value = PASSWORD

# Submit the form
browser.submit_form(signup_form)

browser.open("https://github.com/settings/emails")

for tag in browser.select("#settings-emails > li > span.css-truncate-target"):
    print(tag.text)
