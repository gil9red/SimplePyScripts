#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mvantellingen/python-zeep


# pip install zeep
from zeep import Client


# client = Client('http://www.webservicex.net/ConvertSpeed.asmx?WSDL')
# result = client.service.ConvertSpeed(100, 'kilometersPerhour', 'milesPerhour')
#
# print(result)
# assert result == 62.137


client = Client("http://regexlib.com/WebServices.asmx?WSDL")

result = client.service.ListAllAsXml(maxrows=4)
print(result)
