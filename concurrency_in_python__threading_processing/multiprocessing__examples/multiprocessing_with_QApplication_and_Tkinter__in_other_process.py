#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from multiprocessing import Process
    from multiprocessing__QApplication__in_other_process import go as go_qt
    from multiprocessing__Tkinter__in_other_process import go as go_tk

    p1 = Process(target=go_qt, args=('Qt',))
    p1.start()

    p2 = Process(target=go_tk, args=('Tk',))
    p2.start()

    # Необязательно в данном случае -- главный поток все-равно закроется после дочернего
    # p1.join()
    # p2.join()
