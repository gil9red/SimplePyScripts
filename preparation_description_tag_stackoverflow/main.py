#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://gist.github.com/gil9red/6f7648c9dfc446083d46


"""Используется вместе с SimplePyScripts\Grab\empty_tags_stackoverflow.py
Скрипт empty_tags_stackoverflow.py собирает найденные пустые теги и выводит их в консоль.

В итоге получилось множество такого вида. Второй и третий параметр -- отсутствие руководства и отсутствие описания
тега:

tag_list = {('history', True, True, 'http://ru.stackoverflow.com/tags/history/info'),
            ('suse', True, True, 'http://ru.stackoverflow.com/tags/suse/info'),
            ('qbasic', True, True, 'http://ru.stackoverflow.com/tags/qbasic/info'),
            ...


И это множество тегов было сохранено в виде файлов. Для каждого тега был создан отдельный файл вида:

<tag>
    <name></name>
    <url></url>
    <ref_guide></ref_guide>
    <description></description>
</tag>


"""


# import glob
#
# import os
# import re
#
# from lxml import etree
#
#
# for tag in glob.glob('tags/*.tag'):
#     print(tag)
#
#     parser = etree.XMLParser(remove_blank_text=True)
#     tree = etree.parse(tag, parser)
#     with open(tag, mode='wb') as f:
#         f.write(etree.tostring(tree, pretty_print=True))
