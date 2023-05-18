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

    else:
        return None


# NOTE: before execute this, run append_to_remote_repo.py
if __name__ == "__main__":
    from common import get_repo

    repo = get_repo()
    print(repo)
    print()

    file_name = get_random_file(repo)
    if file_name:
        file_name = os.path.basename(file_name)
        message = "Remove: " + file_name
        print(message)

        repo.index.remove([file_name])
        repo.index.commit(message)

        repo.remotes.origin.push()
