#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    city = 'Magnitogorsk'
    query = "select item from weather.forecast where woeid in (select woeid from geo.places(1) where text='{}') and u='c'".format(city)
    url = "https://query.yahooapis.com/v1/public/yql?q={}&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(query)

    import requests
    rs = requests.get(url)
    item = rs.json()['query']['results']['channel']['item']
    for forecast in item['forecast']:
        print('{date}: {low} - {high}. {day}: {text}'.format(**forecast))

