#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/timeout_block/main.py
############################################################################################################
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


def timeout(seconds=None, raise_timeout=False):
    def wrapper(function_to_decorate):
        def the_wrapper_around_the_original_function(*args, **kwargs):
            thread = KThread(target=lambda: function_to_decorate(*args, **kwargs))
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                thread.kill()

                if raise_timeout:
                    raise TimeoutError()

        return the_wrapper_around_the_original_function

    return wrapper


############################################################################################################


if __name__ == "__main__":
    import random
    import sorts

    from timeit import default_timer

    items = list(range(10**3))
    random.shuffle(items)

    time_by_algo_name = dict()

    for name, algo in sorted(sorts.ALGO_LIST.items(), key=lambda x: x[0]):
        print(name)

        @timeout(seconds=10, raise_timeout=True)
        def run():
            new_items = list(items)
            algo(new_items)

        t = default_timer()
        try:
            run()

        except TimeoutError:
            print("    timeout!")

        except Exception as e:
            print(f"    Error: {e}: sort: {name}")

        t = default_timer() - t
        time_by_algo_name[t] = name
        # print('    duration: {:.3f} secs'.format(t))

    print()
    print("Sorted by time:")
    for t, name in sorted(time_by_algo_name.items(), key=lambda x: x[0]):
        print(f"{name}: {t:.3f} secs")
