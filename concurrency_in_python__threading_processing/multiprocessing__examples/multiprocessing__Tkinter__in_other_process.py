#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def go(name):
    import tkinter as tk
    app = tk.Tk()
    app.minsize(150, 50)

    mw = tk.Label(app, text='Hello, ' + name)
    mw.pack(fill='both', expand=True)

    app.mainloop()


if __name__ == '__main__':
    from multiprocessing import Process
    p = Process(target=go, args=('bob',))
    p.start()

    # Необязательно в данном случае -- главный поток все-равно закроется после дочернего
    # p.join()
