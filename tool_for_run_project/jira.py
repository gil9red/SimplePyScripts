#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import webbrowser


if len(sys.argv) != 2:
    print('Example: jira TXI-926')
    sys.exit()

jira = sys.argv[1].strip()
url = 'https://jira.compassplus.ru/browse/' + jira
print('Open url:', url)

webbrowser.open(url)
