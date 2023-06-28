#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://www.linux.org.ru/forum/development/5632316#comment-5632394


import sys
from threading import Thread


class Kill(Exception):
    pass


class KThread(Thread):
    def __init__(self, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        try:
            self.__run_backup()
        except Kill:
            pass

        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == "call":
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == "line":
                raise Kill()
        return self.localtrace

    def kill(self):
        self.killed = True


if __name__ == "__main__":
    import time

    def unlimited_wait():
        i = 0

        while True:
            i += 1
            print(i)
            time.sleep(1)

    thread = KThread(target=unlimited_wait)
    thread.start()
    thread.join(timeout=10)

    if thread.is_alive():
        thread.kill()
