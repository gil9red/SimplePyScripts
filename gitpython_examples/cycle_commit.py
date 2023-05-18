#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys
import time

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
sys.path.append("../wait")
from wait import wait

from common import get_repo


if __name__ == "__main__":
    repo = get_repo()
    new_file_name = os.path.join(repo.working_tree_dir, "cycle_file")

    while True:
        try:
            repo.remotes.origin.pull()

            if not os.path.exists(new_file_name):
                number = 0
                print(number)

                message = "Start cycle #{}".format(number)

            else:
                with open(new_file_name, "r") as f:
                    number = int(f.read())
                    number += 1

                    print(number)

                message = "Cycle commit #{}".format(number)

            # Обновление значения
            with open(new_file_name, "w") as f:
                f.write(str(number))

            print(message)
            repo.index.add([new_file_name])
            repo.index.commit(message)

        except Exception as e:
            print(e)
            time.sleep(30)

        while True:
            try:
                repo.remotes.origin.push()
                print("Finish push")
                break

            except Exception as e:
                print(e)
                time.sleep(30)

        # Every 1 hour
        wait(hours=1)
