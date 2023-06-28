#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"



from robobrowser import RoboBrowser


browser = RoboBrowser(parser="lxml")
browser.open("http://www.prog.org.ru/index.php")

signup_form = browser.get_form()
signup_form["user"].value = "LOGIN"
signup_form["passwrd"].value = "PASSWORD"

# Submit the form
browser.submit_form(signup_form)

# Тут будет url перенаправления по которому нужно снова перейти
browser.open(browser.response.url)

print("Здравствуйте," in browser.response.text)
print(browser.select(".titlebg2")[0].text.strip())
