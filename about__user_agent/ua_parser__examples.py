#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/ua-parser/uap-python


import pprint

# pip install ua-parser
from ua_parser import user_agent_parser


ua_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
            '(KHTML, like Gecko) Chrome/61.0.3347.109 Safari/537.36'


pp = pprint.PrettyPrinter(indent=4)

parsed_string = user_agent_parser.Parse(ua_string)
pp.pprint(parsed_string)
# {   'device': {'brand': None, 'family': 'Other', 'model': None},
#     'os': {   'family': 'Windows',
#               'major': '10',
#               'minor': None,
#               'patch': None,
#               'patch_minor': None},
#     'string': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#               '(KHTML, like Gecko) Chrome/61.0.3347.109 Safari/537.36',
#     'user_agent': {   'family': 'Chrome',
#                       'major': '61',
#                       'minor': '0',
#                       'patch': '3347'}}

parsed_string = user_agent_parser.ParseUserAgent(ua_string)
pp.pprint(parsed_string)
# {'family': 'Chrome', 'major': '61', 'minor': '0', 'patch': '3347'}

parsed_string = user_agent_parser.ParseOS(ua_string)
pp.pprint(parsed_string)
# {   'family': 'Windows',
#     'major': '10',
#     'minor': None,
#     'patch': None,
#     'patch_minor': None}

parsed_string = user_agent_parser.ParseDevice(ua_string)
pp.pprint(parsed_string)
# {'brand': None, 'family': 'Other', 'model': None}
