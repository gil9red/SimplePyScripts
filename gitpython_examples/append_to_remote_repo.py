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
    from common import get_repo, print_log

    repo = get_repo()
    print(repo)
    print()

    print_log()

    print()

    new_file_name = create_random_file(repo)[1]
    message = "Create: " + new_file_name
    print(message)

    repo.index.add([new_file_name])
    # # or:
    # repo.index.add(['*'])
    # repo.git.add(new_file_name)
    # repo.git.add('-A')

    repo.index.commit(message)

    # repo.remotes.origin.pull()
    repo.remotes.origin.push()
