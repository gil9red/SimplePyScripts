#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

# pip install GitPython
import git

from common import get_total_commits


def process_repository(repo_path: Path) -> None:
    print(repo_path)

    repo = git.Repo(repo_path)
    urls = list(repo.remotes.origin.urls)
    print(f'Urls: {", ".join(urls)}')

    old_number_commits = get_total_commits(repo)

    repo.remotes.origin.pull()

    new_number_commits = get_total_commits(repo)
    diff = new_number_commits - old_number_commits
    if diff > 0:
        print(f"New commits: {diff}")
    else:
        print(f"Repository is actual")


def process_all(path: Path, pattern: str = '.git') -> None:
    paths: list[Path] = [
        p.parent
        for p in path.rglob(pattern)
        if p.is_dir()
    ]

    for repo_path in paths:
        try:
            process_repository(repo_path)
        except Exception as e:
            print(f'Error: {e}')

        print()


if __name__ == '__main__':
    path = Path.home() / 'PycharmProjects'
    process_all(path)
