#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

# pip install jinja2
import jinja2


@dataclass
class User:
    username: str
    url: str


template = jinja2.Template(
    """\
<title>{{ title }}</title>
<ul>
{% for user in users %}
  <li><a href="{{ user.url }}">{{ user.username }}</a></li>
{% endfor %}
</ul>
"""
)

users = [
    User("1", "https://a.bc/user/1"),
    User("2", "https://a.bc/user/2"),
    User("3", "https://a.bc/user/3"),
]

html = template.render(title="Hello World!", users=users)
print(html)
