#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import string
import os
import uuid


def create_random_file(repo):
    file_name = str(uuid.uuid4())
    full_file_name = os.path.join(repo.working_tree_dir, file_name)

    with open(full_file_name, "w") as f:
        text = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(64)
        )
        f.write(text)

    return file_name, file_name


if __name__ == "__main__":
    import api

    repo = api.repo
    print(repo)
    print()

    api.print_log()
    print()

    file_name = create_random_file(repo)[1]
    message = "Create: " + file_name
    print(message)

    api.append(file_name)
    api.commit(message)

    # api.pull()
    # repo.remotes.origin.pull()
    api.push()
