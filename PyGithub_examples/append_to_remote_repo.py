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


from config import LOGIN, PASSWORD


# pip install PyGitHub
import github
gh = github.Github(LOGIN, PASSWORD)
user = gh.get_user()

NEW_REPO = 'Test-Repo'

try:
    repo = user.get_repo(NEW_REPO)

except:
    repo = user.create_repo(NEW_REPO)

print(repo)
url_git = repo.svn_url

import os
repo_name = os.path.basename(url_git)
repo_path = os.path.abspath(repo_name)

# pip install GitPython
import git

try:
    repo = git.Repo(repo_path)
except:
    repo = git.Repo.clone_from(url_git, repo_path)

print(repo)
print()

logs = list(repo.head.log())
print('Logs[{}]:'.format(len(logs)))
for log in logs:
    print(str(log).strip())
print()

# new_file_name = create_random_file(repo)[1]
# print(new_file_name)
#
# repo.index.add([new_file_name])
# # # or:
# # repo.index.add(['*'])
# # repo.git.add(new_file_name)
# # repo.git.add('-A')
#
# repo.index.commit("Commit " + new_file_name)

# repo.remotes.origin.push()

# ilya.petrash@inbox.ru
# repo.git.config('--global', "user.name", "user name")
# repo.git.config('--global', "user.email", "user@domain.com")

# How generate id_rsa:
# https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
# git-bash: ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# passphrase is empty
#
# Append id_rsa.pub in repo settings in Deploy keys
#
# Magic:
# git remote set-url origin git@github.com:gil9red/Test-Repo.git
# GIT_SSH_COMMAND='ssh -i ~/.ssh/id_rsa' git push --porcelain origin
# or:
# GIT_SSH_COMMAND='ssh -i C:/Users/ipetrash/Desktop/PyScripts/SimplePyScripts/PyGithub_examples/Test-Repo/id_rsa' git push --porcelain origin
#
#
# Old https url:
# git remote set-url origin https://github.com/gil9red/Test-Repo


with repo.git.custom_environment(GIT_SSH_COMMAND='ssh -i ~/.ssh/id_rsa'):
    origin = repo.remotes.origin
    origin.push()


# repo.remotes.origin.pull()
# repo.remotes.origin.push(repo.head)
