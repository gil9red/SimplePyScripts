#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


"""
Получение всех постов группы https://vk.com/farguscovers
"""


from vk_api import VkTools
from root_common import get_vk_session


DOMAIN = "farguscovers"


vk_session = get_vk_session()
tools = VkTools(vk_session)

data = {
    "domain": DOMAIN,
}
wall_it = tools.get_all_iter("wall.get", 100, data)
for i, item in enumerate(wall_it, 1):
    print(i, item)
