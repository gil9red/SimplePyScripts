#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# url = 'http://opendata.mkrf.ru/opendata/7705851331-register_movies/data-16-structure-3.json'
#
# import requests
# rs = requests.get(url)
#
# with open('data-16-structure-3.json', mode='wb') as f:
#     f.write(rs.content)


# TODO: append sqlite: https://github.com/gil9red/SimplePyScripts/blob/bd30048f16679789fc366e41ffc57cba71c032c9/games_with_denuvo/common.py

import json
json_data = json.load(open('data-16-structure-3.json', 'r', encoding='utf-8'))
# print(len(json_data))
# print(json.dumps(json_data[0], indent=4, ensure_ascii=False))
for film in json_data:
    print(film)
    info = film['data']['general']
    
    print('Название фильма:', info.get('filmname'))
    print('Наименование на иностранном языке:', info.get('foreignName'))
    print('Режиссер:', info.get('director'))
    print('Жанр:', info.get('viewMovie'))
    print('Студия-производитель:', info.get('studio'))
    print('Год производства:', info.get('crYearOfProduction'))
    print('Количество серий:', info.get('numberOfSeries'))
    print('Продолжительность показа, минуты:', info.get('durationMinute'))
    print('Цвет:', info['color'])
    print('Возрастная категория зрительской аудитории:', info.get('ageCategory'))
    print('Аннотация:', info.get('annotation'))
    print('Страна производства:', info.get('countryOfProduction'))
    print()
