#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from lxml import html


root = html.fromstring("<p>Hello<br>world!</p><br>")

print(html.tostring(root))  # b'<div><p>Hello<br>world!</p><br></div>'
print(html.tostring(root, encoding="unicode"))  # <div><p>Hello<br>world!</p><br></div>
print(
    html.tostring(root, pretty_print=True)
)  # b'<div>\n<p>Hello<br>world!</p>\n<br>\n</div>\n'
print(html.tostring(root, encoding="unicode", pretty_print=True))
# <div>
# <p>Hello<br>world!</p>
# <br>
# </div>
