#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import requests

# # rs = requests.get('http://127.0.0.1:5000/get_news_list/games?last=2')
# # rs = requests.get('http://127.0.0.1:5000/get_news_list/games?last=-1')
# # rs = requests.get('http://127.0.0.1:5000/get_news_list?last=2')
# # rs = requests.get('http://127.0.0.1:5000/get_news_list')
# rs = requests.get('http://127.0.0.1:5000/get_news_list/games')
# # rs = requests.get('http://127.0.0.1:5000/get_news_list/games?last=5')
#
# rs_json = rs.json()
# print(rs_json)
# print('  count={count} total={total}'.format(**rs_json))
#
# if not rs_json['count']:
#     print('Новостей нет')
#
# for interest, news_list in rs_json['items'].items():
#     print('{} ({}):'.format(interest, len(news_list)))
#
#     for i, news in enumerate(news_list, 1):
#         print("    {}. {}: {}".format(i, news['title'], news['url']))
#
#
# quit()


# # Пример опроса сервера о новых новостях
# rs = requests.get('http://127.0.0.1:5000/reset_all_is_read')

while True:
    rs = requests.get(
        "http://127.0.0.1:5000/get_news_list_and_mark_as_read/games?count=3"
    )

    rs_json = rs.json()
    print(rs_json)
    print("  count={count} total={total}".format(**rs_json))

    if not rs_json["count"]:
        print("Новостей нет")

    else:
        for interest, news_list in rs_json["items"].items():
            print("{} ({}):".format(interest, len(news_list)))

            for i, news in enumerate(news_list, 1):
                print("    {}. {}: {}".format(i, news["title"], news["url"]))

        print()

    # Ждем 5 минут
    time.sleep(60 * 5)
