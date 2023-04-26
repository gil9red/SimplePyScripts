#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import Process, Manager


def f(users_data):
    users_data["users"][0]["coins"] += 1


if __name__ == "__main__":
    manager = Manager()
    users_data = manager.dict()
    user_data = manager.dict({"id": 1, "coins": 0})
    users_data["users"] = manager.list([user_data])

    p = Process(target=f, args=[users_data])
    p.start()
    p.join()
    print(users_data["users"][0])
    # {'id': 1, 'coins': 1}
