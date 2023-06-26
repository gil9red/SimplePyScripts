#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import time

# pip install simple-wait
from simple_wait import wait

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

                message = f"Start cycle #{number}"

            else:
                with open(new_file_name, "r") as f:
                    number = int(f.read())
                    number += 1

                    print(number)

                message = f"Cycle commit #{number}"

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
