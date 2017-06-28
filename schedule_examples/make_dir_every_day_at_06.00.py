#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def job():
    from datetime import date
    print(date.today())

    try:
        import os
        os.mkdir(r'T:\ipetrash')

    except FileExistsError:
        pass


if __name__ == '__main__':
    # pip install schedule
    import schedule
    schedule.every().day.at("6:00").do(job)

    while True:
        schedule.run_pending()

        import time
        time.sleep(1)
