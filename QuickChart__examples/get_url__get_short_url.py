#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_chart


qc = get_chart()
print(qc.get_url())
# https://quickchart.io/chart?c=%7B%22type%22%3A%22doughnut%22%2C%22data%22%3A%7B%22datasets%22%3A%5B%7B%22data%22%3A%5B43%2C21%5D%2C%22backgroundColor%22%3A%5B%22rgb%28173+225+232%29%22%2C%22rgb%2833+170+184%29%22%5D%2C%22borderWidth%22%3A0%7D%5D%7D%2C%22options%22%3A%7B%22cutoutPercentage%22%3A80%2C%22legend%22%3A%7B%22display%22%3A%22false%22%7D%2C%22plugins%22%3A%7B%22datalabels%22%3A%7B%22display%22%3A%22false%22%7D%7D%7D%7D&w=500&h=300&bkg=&devicePixelRatio=1.0&f=png&v=2

print(qc.get_short_url())
# https://quickchart.io/chart/render/sf-9237a1bc-f7ce-4156-ac58-2452a5729e9e
