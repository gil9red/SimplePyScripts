#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# from multiprocessing import Process
from threading import Thread
from notifications import WindowsBalloonTip


def run(title: str, text: str, duration: int = 20):
    WindowsBalloonTip.balloon_tip(title, text, duration)


# def run_in_process(title: str, text: str, duration: int = 20):
#     Process(target=run, args=(title, text, duration)).start()


def run_in_thread(title: str, text: str, duration: int = 20):
    Thread(target=run, args=(title, text, duration)).start()


if __name__ == '__main__':
    run_in_thread('Уведомление1', 'Проверь!!!!')
    run_in_thread('Уведомление2', 'Проверь!!!!')
    run_in_thread('Уведомление3', 'Проверь!!!!')
    # Process(target=run, args=('Уведомление', 'Проверь!!!!'), daemon=True).start()
    # run_in_process('Уведомление', 'Проверь 2!!!!')
    # Process(target=run, args=('Уведомление', 'Проверь 3!!!!'), daemon=True).start()
    #
    # import time
    # time.sleep(5)
