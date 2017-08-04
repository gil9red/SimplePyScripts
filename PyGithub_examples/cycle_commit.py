#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import LOGIN, PASSWORD

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


def wait(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    from datetime import timedelta, datetime
    today = datetime.today()
    timeout_date = today + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )

    while today <= timeout_date:
        def str_timedelta(td):
            # Remove ms
            td = str(td)
            if '.' in td:
                td = td[:td.index('.')]

            return td

        left = timeout_date - today
        left = str_timedelta(left)

        print('\r' * 100, end='')
        print('До следующего запуска осталось {}'.format(left), end='')

        import sys
        sys.stdout.flush()

        # Delay 1 seconds
        import time
        time.sleep(1)

        today = datetime.today()

    print('\r' * 100, end='')
    print('\n')


if __name__ == '__main__':
    repo = get_repo()

    new_file_name = os.path.join(repo.working_tree_dir, 'cycle_file')

    while True:
        repo.remotes.origin.pull()

        if not os.path.exists(new_file_name):
            number = 0
            print(number)

            message = "Start cycle #{}".format(number)

        else:
            with open(new_file_name, 'r') as f:
                number = int(f.read())
                number += 1

                print(number)

            message = "Cycle commit #{}".format(number)

        # Обновление значения
        with open(new_file_name, 'w') as f:
            f.write(str(number))

        print(message)
        repo.index.add([new_file_name])
        repo.index.commit(message)

        repo.remotes.origin.push()
        print('Finish push')

        # Every 1 hour
        wait(hours=1)

        print()
