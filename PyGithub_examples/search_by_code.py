#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from base64 import b64decode as base64_to_text

# pip install pygithub
from github import Github

from config import LOGIN, PASSWORD


gh = Github(LOGIN, PASSWORD)
# print(list(gh.search_code('requests auth github filename:.py language:python')[:5]))

search_query = "requests auth github filename:.py language:python"
# print(gh.search_code(search_query).totalCount)

# The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and
# secret, you can make up to 30 requests per minute. For unauthenticated requests, the rate limit allows
# you to make up to 10 requests per minute.
#
# Если авторизован, то каждые 2 секунды можно слать запрос, иначе каждые 6
timeout = 2 if LOGIN and PASSWORD else 6

# Немного добавить на всякий
timeout += 0.5

import time

search_result = gh.search_code(search_query)
total_count = search_result.totalCount
page = 0

data = search_result.get_page(page)
print(data[0])
print(dir(data[0]))
print(data[0].url)
print(data[0].content)

print(base64_to_text(data[0].content.encode()).decode())
print(data[0].html_url)

# get user from repo url
user = data[0].html_url.split("/")[3]
print(user)

# i = 1
# while total_count > 0:
#     data = search_result.get_page(page)
#     for result in data:
#         print(i, result)
#         i += 1
#
#     print('page: {}, total: {}, results: {}'.format(page, total_count, len(data)))
#     page += 1
#     total_count -= len(data)
#
#     # Задержка запросов, чтобы гитхаб не блокировал временно доступ
#     time.sleep(timeout)


# i = 1
# for match in gh.search_code(search_query):
#     print(i, match)
#     i += 1
#
#     time.sleep(timeout)
#
#     # print(dir(match))
#     # break
