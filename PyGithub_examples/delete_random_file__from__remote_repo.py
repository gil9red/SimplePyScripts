#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_random_file(repo):
    file_names = list()

    import os
    for root, dirs, files in os.walk(repo.working_tree_dir):
        if '.git' in root:
            continue

        for file in files:
            file_names.append(os.path.join(root, file))

    if file_names:
        import random
        return random.choice(file_names)

    else:
        return None


from config import LOGIN, PASSWORD

# NOTE:
NEW_REPO = 'Test-Repo'

import os
REPO_PATH = os.path.abspath(NEW_REPO)

# How use without input login and password:
# git clone https://username:password@github.com/username/repository.git
URL_GIT = 'https://{0}:{1}@github.com/{0}/{2}.git'.format(LOGIN, PASSWORD, NEW_REPO)


def get_repo():
    # pip install GitPython
    import git

    try:
        return git.Repo(REPO_PATH)

    except:
        return git.Repo.clone_from(URL_GIT, REPO_PATH)


# NOTE: first execute append_to_remote_repo.py
if __name__ == '__main__':
    repo = get_repo()
    print(repo)
    print()

    file_name = get_random_file(repo)
    if file_name:
        file_name = os.path.basename(file_name)
        message = 'Remove: ' + file_name
        print(message)

        repo.index.remove([file_name])
        repo.index.commit(message)

        repo.remotes.origin.push()
