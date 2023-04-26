#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import random


def get_random_file(repo):
    file_names = []

    for root, dirs, files in os.walk(repo.working_tree_dir):
        if ".git" in root:
            continue

        for file in files:
            file_names.append(os.path.join(root, file))

    if file_names:
        return random.choice(file_names)

    return


# NOTE: first execute append_to_remote_repo.py
if __name__ == "__main__":
    import api

    repo = api.repo
    print(repo)
    print()

    api.print_log()
    print()

    abs_file_name = get_random_file(repo)
    if abs_file_name:
        file_name = os.path.basename(abs_file_name)
        message = "Remove: " + file_name
        print(message)

        api.remove(file_name)
        api.commit(message)

        api.push()

        os.remove(abs_file_name)
