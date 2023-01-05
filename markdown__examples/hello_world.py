#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install markdown
import markdown


text_markdown = """
*Hello* **[World](https://ru.wikipedia.org/wiki/Hello,_world!)**!
""".strip()
text_html = markdown.markdown(text_markdown)
print(text_html)
# <p><em>Hello</em> <strong><a href="https://ru.wikipedia.org/wiki/Hello,_world!">World</a></strong>!</p>
