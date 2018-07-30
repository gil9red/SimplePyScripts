#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import lxml.html


def to_string(node):
    return lxml.html.tostring(node, encoding='unicode')


text = """<div id="game_area_description" class="game_area_description">
<strong>Самая популярная игра в Steam</strong>
<br>Ежедневно миллионы игроков по всему миру вступают в битву от лица одного....."""

html = lxml.html.fromstring(text)
game_descriptions = html.cssselect('#game_area_description')[0]

inner_html = ''.join(to_string(child) for child in game_descriptions.iterchildren())
print(inner_html)
