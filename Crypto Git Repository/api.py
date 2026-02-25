#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install GitPython
import git

from config import REPO_PATH, URL_GIT


repo = None


def __get_repo():
    try:
        return git.Repo(REPO_PATH)

    except:
        return git.Repo.clone_from(URL_GIT, REPO_PATH)


def get_repo():
    global repo
    if repo:
        return repo

    repo = __get_repo()
    return repo


repo = get_repo()


def print_log(reverse=False) -> None:
    logs = repo.git.log("--pretty=format:%H%x09%an%x09%ad%x09%s").splitlines()
    print(f"Logs[{len(logs)}]:")

    if reverse:
        logs.reverse()

    for log in logs:
        print(log)


def append(file_or_list) -> None:
    if type(file_or_list) == str:
        file_or_list = [file_or_list]

    repo.index.add(file_or_list)


def remove(file_or_list) -> None:
    if type(file_or_list) == str:
        file_or_list = [file_or_list]

    repo.index.remove(file_or_list)


def commit(message) -> None:
    repo.index.commit(message)


def pull() -> None:
    repo.remotes.origin.pull()


def push() -> None:
    repo.remotes.origin.push()
