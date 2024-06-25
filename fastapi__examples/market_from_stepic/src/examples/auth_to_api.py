#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import urllib.request
import urllib.parse


URL = "http://127.0.0.1:7777"


def get_token(username: str, password: str) -> str:
    login_data = {
        "username": username,
        "password": password,
    }

    req = urllib.request.Request(
        f"{URL}/api/v1/token",
        method="POST",
        data=urllib.parse.urlencode(login_data).encode("utf-8"),
    )
    with urllib.request.urlopen(req) as rs:
        rs_data = json.loads(rs.read().decode("utf-8"))
        return rs_data["token"]


def get_users(token: str) -> dict[str, dict]:
    req = urllib.request.Request(
        f"{URL}/api/v1/users",
        method="GET",
    )
    req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req) as rs:
        return json.loads(rs.read().decode("utf-8"))


if __name__ == "__main__":
    token = get_token(username="admin", password="Admin_4321!")
    print(token)
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyOWFlN2ViZi00NDQ1LTQyZjItOTU0OC1hM2E1NGYwOTUyMjAiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MjE5MTg0MTh9.rTETSqUw0hRWJQFrBcHo9NiHwhfeUqZ0brDMuPp70xw

    print(get_users(token))
    # {'items': [{'id': '29ae7ebf-4445-42f2-9548-a3a54f095220', 'role': 'admin', 'username': 'admin'}]}
