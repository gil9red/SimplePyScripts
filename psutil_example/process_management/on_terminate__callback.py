#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Run 2 process and wait terminate


def func(time_life=4):
    import time
    i = 1

    import threading

    while i <= time_life:
        print(threading.current_thread(), i)
        i += 1

        time.sleep(1)


if __name__ == "__main__":
    from multiprocessing import Process
    p1 = Process(target=func, args=(5,))
    p1.start()

    p2 = Process(target=func, args=(9,))
    p2.start()

    # pip install psutil
    import psutil
    process1 = psutil.Process(p1.pid)
    print("process1 is_running:", process1.is_running())

    process2 = psutil.Process(p2.pid)
    print("process2 is_running:", process2.is_running())
    print()

    def on_terminate(proc):
        print('Process "{}" terminated'.format(proc))

    # waits for multiple processes to terminate
    gone, alive = psutil.wait_procs(
        [process1, process2], timeout=30, callback=on_terminate
    )
    print()
    print("gone:", gone)
    print("alive:", alive)
