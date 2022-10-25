#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import time

from pathlib import Path
from typing import Union


DIRS = [r'C:\DEV__TX', r'C:\DEV__OPTT', r'C:\DEV__RADIX']


def run(dirs: list[Union[str, Path]]):
    print(f'\n{DT.datetime.today()}')

    for dir_path in dirs:
        print(dir_path)
        for file_name in Path(dir_path).glob('*/hs_err_pid*.log'):
            ctime_timestamp = file_name.stat().st_ctime
            ctime = DT.datetime.fromtimestamp(ctime_timestamp)
            print(f'{file_name} (date creation: {ctime})')

            # Удаление, если с даты создания прошло больше 1 дня
            if DT.datetime.today() > ctime + DT.timedelta(days=1):
                file_name.unlink(missing_ok=True)


if __name__ == '__main__':
    while True:
        run(DIRS)
        time.sleep(5 * 60 * 60)
