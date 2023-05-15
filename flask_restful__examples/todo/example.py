#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


URL_BASE = "http://127.0.0.1:5000"


url = URL_BASE
print(f"GET: {url}")
rs = requests.get(url)
print(rs, rs.json())
"""
GET: http://127.0.0.1:5000
<Response [200]> {'total': 3}
"""

print()

url = f"{URL_BASE}/todos"
print(f"GET: {url}")
rs = requests.get(url)
rs_json = rs.json()
print(rs, rs_json)
"""
GET: http://127.0.0.1:5000/todos
<Response [200]> {'todo1': {'task': 'build an API'}, 'todo2': {'task': '?????'}, 'todo3': {'task': 'profit!'}}
"""

print()

todo_id = list(rs_json)[0]

url = f"{URL_BASE}/todos/{todo_id}"
print(f"GET: {url}")
rs = requests.get(url)
print(rs, rs.json())
"""
GET: http://127.0.0.1:5000/todos/todo1
<Response [200]> {'task': 'build an API'}
"""

print()

url = f"{URL_BASE}/todos/{todo_id}"
print(f"PUT: {url}")
rs = requests.put(url, json=dict(task=f"Update task {todo_id}"))
print(rs, rs.json())
"""
PUT: http://127.0.0.1:5000/todos/todo1
<Response [201]> {'task': 'Update task todo1'}
"""

print()

url = f"{URL_BASE}/todos/{todo_id}_new"
print(f"PUT: {url}")
rs = requests.put(url, json=dict(task=f"New task!"))
print(rs, rs.json())
"""
PUT: http://127.0.0.1:5000/todos/todo1_new
<Response [201]> {'task': 'New task!'}
"""

print()

url = f"{URL_BASE}/todos"
print(f"POST: {url}")
rs = requests.post(url, json=dict(task=f"New task!"))
print(rs, rs.json())
"""
POST: http://127.0.0.1:5000/todos
<Response [201]> {'task': 'New task!'}
"""

print()

url = f"{URL_BASE}/todos"
print(f"GET: {url}")
rs = requests.get(url)
print(rs, rs.json())
"""
GET: http://127.0.0.1:5000/todos
<Response [200]> {'todo1': {'task': 'Update task todo1'}, 'todo2': {'task': '?????'}, 'todo3': {'task': 'profit!'}, 'todo1_new': {'task': 'New task!'}, 'todo5': {'task': 'New task!'}}
"""

print()

url = f"{URL_BASE}/todos/{todo_id}"
print(f"DELETE: {url}")
rs = requests.delete(url)
print(rs, rs.json())
"""
DELETE: http://127.0.0.1:5000/todos/todo1
<Response [200]> {'ok': True}
"""

print()

url = f"{URL_BASE}/todos"
print(f"GET: {url}")
rs = requests.get(url)
print(rs, rs.json())
"""
GET: http://127.0.0.1:5000/todos
<Response [200]> {'todo2': {'task': '?????'}, 'todo3': {'task': 'profit!'}, 'todo1_new': {'task': 'New task!'}, 'todo5': {'task': 'New task!'}}
"""

print()

url = URL_BASE
print(f"GET: {url}")
rs = requests.get(url)
print(rs, rs.json())
"""
GET: http://127.0.0.1:5000
<Response [200]> {'total': 4}
"""
