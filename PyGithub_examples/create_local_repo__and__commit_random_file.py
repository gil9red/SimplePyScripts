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


FILE_NAME_REPO = 'Test-Repo'


if __name__ == '__main__':
    import os
    repo_path = os.path.abspath(FILE_NAME_REPO)

    import git
    try:
        repo = git.Repo(FILE_NAME_REPO)
    except:
        repo = git.Repo.init(FILE_NAME_REPO)

    print('Repo:', repo)
    print()

    logs = list(repo.head.log())
    print('Logs[{}]:'.format(len(logs)))
    for log in logs:
        print(str(log).strip())
    print()

    new_file_name = create_random_file(repo)[1]
    print('Append: ' + new_file_name)

    repo.index.add([new_file_name])
    # or:
    # repo.git.add(new_file_name)
    # # or:
    # # repo.git.add('-A')

    repo.index.commit("Commit " + new_file_name)
