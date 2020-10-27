#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://gist.github.com/benhoyt/8c8a8d62debe8e5aa5340373f9c509c7

"""An atomic, thread-safe incrementing counter."""

import threading


class AtomicCounter:
    """An atomic, thread-safe incrementing counter.

    >>> counter = AtomicCounter()
    >>> counter.increment()
    1
    >>> counter.increment(4)
    5

    >>> counter = AtomicCounter(42.5)
    >>> counter.value
    42.5
    >>> counter.increment(0.5)
    43.0

    >>> counter = AtomicCounter()
    >>> def incrementor():
    ...     for i in range(100000):
    ...         counter.increment()
    >>> threads = []
    >>> for i in range(4):
    ...     thread = threading.Thread(target=incrementor)
    ...     thread.start()
    ...     threads.append(thread)
    >>> for thread in threads:
    ...     thread.join()
    >>> counter.value
    400000
    """
    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self.value = initial
        self._lock = threading.Lock()

    def increment(self, num=1):
        """Atomically increment the counter by num (default 1) and return the
        new value.
        """
        with self._lock:
            self.value += num
            return self.value


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # MORE:
    NUM = 100000
    NUM_THREADS = 4

    counter = AtomicCounter()

    def incrementor():
        for i in range(NUM):
            counter.increment()

    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=incrementor)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(counter.value)
    assert counter.value == NUM * NUM_THREADS
