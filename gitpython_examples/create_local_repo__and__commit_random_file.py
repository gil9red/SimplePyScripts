#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import string
import os
import uuid

# pip install GitPython
import git


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


FILE_NAME_REPO = "Test-Repo"


if __name__ == "__main__":
    repo_path = os.path.abspath(FILE_NAME_REPO)

    try:
        repo = git.Repo(FILE_NAME_REPO)
    except:
        repo = git.Repo.init(FILE_NAME_REPO)

    print("Repo:", repo)
    print()

    logs = repo.git.log("--pretty=format:%H%x09%an%x09%ad%x09%s").splitlines()
    print(f"Logs[{len(logs)}]:")

    for log in logs:
        print(log)

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
