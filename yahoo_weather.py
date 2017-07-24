#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    city = "Магнитогорск"
    # # OR:
    # city = 'Magnitogorsk'
    url = "https://query.yahooapis.com/v1/public/yql?q=select item from weather.forecast where woeid in " \
          "(select woeid from geo.places(1) where text='{city}') and u='c'" \
          "&format=json&diagnostics=true".format(city=city)

    import requests
    rs = requests.get(url)
    item = rs.json()['query']['results']['channel']['item']

    # https://developer.yahoo.com/weather/documentation.html in Condition Codes
    # code = condition['code']
    #
    # Weather image: http://l.yimg.com/a/i/us/we/52/' + code + '.gif
    # Example: http://l.yimg.com/a/i/us/we/52/26.gif
    #
    condition = item['condition']
    print('Current: {temp} °C, {text}'.format(**condition))
    print()

    print('Forecast:')
    for forecast in item['forecast']:
        print('{date}: {low} - {high} °C. {day}: {text}'.format(**forecast))
