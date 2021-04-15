#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import configparser


ini = configparser.ConfigParser()
ini['Default'] = {
    'x': 10,
    'y': 15,
    'z': 3,
}

ini['Additional'] = {}
additional = ini['Additional']
additional['top'] = str(True)
additional['text'] = "Hello World!"
additional['arrays'] = str([1, 2, 3, 4, 5])

ini['Empty'] = {}

with open('config.ini', 'w') as f:
    ini.write(f)


ini_read = configparser.ConfigParser()
ini_read.read('config.ini')
print(ini_read.sections())

print(ini_read['Additional']['top'])
print(ini_read['Additional']['text'])
print(ini_read['Additional']['arrays'])
print(ini_read['Additional']['arrays'].replace('[', '').replace(']', '').split(', '))
