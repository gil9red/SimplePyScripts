#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def create_random_file(repo):
    import uuid
    file_name = str(uuid.uuid4())

    import os
    full_file_name = os.path.join(repo.working_tree_dir, file_name)

    with open(full_file_name, 'w') as f:
        import random
        import string
        text = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
        f.write(text)

    return file_name, file_name


url_git = 'https://github.com/gil9red/Test-Repo'

import os
repo_name = os.path.basename(url_git)
repo_path = os.path.abspath(repo_name)

import git

try:
    repo = git.Repo(repo_path)
except:
    repo = git.Repo.clone_from(url_git, repo_path)

print(repo)

# new_file_name = create_random_file(repo)[1]
# print(new_file_name)
#
# repo.git.add(new_file_name)
# repo.index.commit("Commit " + new_file_name)


# repo.remotes.origin.pull()
# repo.remotes.origin.push(repo.head)
