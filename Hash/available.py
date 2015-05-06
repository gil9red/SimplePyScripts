__author__ = 'ipetrash'

import hashlib
import sys

if __name__ == '__main__':
    algorithms = list(hashlib.algorithms_available)  # get list algorithms
    algorithms.sort()
    print("Algorithms available: %s" % ", ".join(algorithms))

    text = input("Text: ")
    if not text:
        print("Empty text!")
        sys.exit(1)

    alg = input("Name algorithm: ")
    if not alg in algorithms:  # search in list
        print("Algorithm not found!")
        sys.exit(1)

    hash = hashlib.new(alg)  # create hash function from name
    hash.update(text.encode())  # set data in hash-function
    print("Result:")
    print(" hex: %s" % hash.hexdigest())
    print(" HEX: %s" % hash.hexdigest().upper())
