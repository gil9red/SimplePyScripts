#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/q/1270426/201445


import configparser


config = configparser.ConfigParser()
config.read("example.ini")

print(dict(config["DEFAULT"]))

for section in config.sections():
    print(dict(config[section]))
