#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import os
import shutil
import sys

# If need use threads
from multiprocessing.dummy import Pool
# Or:
# from multiprocessing import Pool

from pathlib import Path

import psutil

sys.path.append(str(Path(__file__).resolve().parent.parent))
from human_byte_size import sizeof_fmt


def search_empty_folders(disk):
    disk_letter = disk[0]
    file_name = f'log of {disk_letter}.txt'

    t = time.perf_counter()

    usage = shutil.disk_usage(disk)
    print(f'  Start of {disk_letter} ({sizeof_fmt(usage.free)} free of {sizeof_fmt(usage.total)})')

    with open(file_name, mode='w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(disk):
            # If dir is empty
            if not dirs and not files:
                f.write(root + '\n')

    print(f'  Finish "{disk_letter}"! Elapsed time: {time.perf_counter() - t:.3f} secs')


if __name__ == '__main__':
    print('Start')

    disk_list = [disk.device for disk in psutil.disk_partitions() if 'fixed' in disk.opts]
    print(f'  Found ({len(disk_list)}): {disk_list}')
    print()

    t = time.perf_counter()

    # Number of thread or process
    worker_number = len(disk_list)

    pool = Pool(worker_number)
    results = pool.map(search_empty_folders, disk_list)

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    print(f'Finish! Elapsed time: {time.perf_counter() - t:.3f} secs')
