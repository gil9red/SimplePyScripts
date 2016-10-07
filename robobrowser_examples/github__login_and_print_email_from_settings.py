#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'


if __name__ == '__main__':
    from robobrowser import RoboBrowser

    browser = RoboBrowser(parser='lxml')
    browser.open('https://github.com/login')

    signup_form = browser.get_form()
    signup_form['login'].value = LOGIN
    signup_form['password'].value = PASSWORD

    # Submit the form
    browser.submit_form(signup_form)

    browser.open('https://github.com/settings/emails')

    for tag in browser.select('#settings-emails > li > span.css-truncate-target'):
        print(tag.text)
