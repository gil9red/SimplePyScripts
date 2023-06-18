#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime


my_bd = datetime.datetime(day=18, month=8, year=1992)
my_life = datetime.datetime.today() - my_bd

print(f"lived time: days = {my_life.days} <=> seconds = {int(my_life.total_seconds())}")
