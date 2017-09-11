#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


class TimeThis(object):
    def __init__(self, title="TimeThis"):
        self.title = title
        self.start_time = None

    def __enter__(self):
        import time
        self.start_time = time.clock()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        import time
        print('[{}] total time: {} sec'.format(self.title, time.clock() - self.start_time))


if __name__ == '__main__':
    with TimeThis():
        import time
        time.sleep(1)

    with TimeThis("Test"):
        text = ''
        for i in range(10 ** 6):
            text += str(i)

    with TimeThis("Test"):
        items = []
        for i in range(10 ** 6):
            items.append(str(i))

        text = ''.join(items)

