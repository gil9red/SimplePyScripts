#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pyxDamerauLevenshtein
# https://github.com/gfairchild/pyxDamerauLevenshtein
# SOURCE: https://github.com/gfairchild/pyxDamerauLevenshtein/blob/master/examples/examples.py


import random
import string
import timeit

import numpy as np
from pyxdameraulevenshtein import (
    damerau_levenshtein_distance,
    normalized_damerau_levenshtein_distance,
    damerau_levenshtein_distance_ndarray,
    normalized_damerau_levenshtein_distance_ndarray,
)


print("# edit distances (low edit distance means words are more similar):")
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "smtih", "smith", damerau_levenshtein_distance("smtih", "smith")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "snapple", "apple", damerau_levenshtein_distance("snapple", "apple")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "testing", "testtn", damerau_levenshtein_distance("testing", "testtn")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "saturday", "sunday", damerau_levenshtein_distance("saturday", "sunday")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "Saturday", "saturday", damerau_levenshtein_distance("Saturday", "saturday")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "orange", "pumpkin", damerau_levenshtein_distance("orange", "pumpkin")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}".format(
        "gifts", "profit", damerau_levenshtein_distance("gifts", "profit")
    )
)
print(
    "damerau_levenshtein_distance('{}', '{}') = {}  # unicode example\n".format(
        "Sjöstedt", "Sjostedt", damerau_levenshtein_distance("Sjöstedt", "Sjostedt")
    )
)  # unicode example

print("# normalized edit distances (low ratio means words are similar):")
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "smtih", "smith", normalized_damerau_levenshtein_distance("smtih", "smith")
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "snapple", "apple", normalized_damerau_levenshtein_distance("snapple", "apple")
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "testing",
        "testtn",
        normalized_damerau_levenshtein_distance("testing", "testtn"),
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "saturday",
        "sunday",
        normalized_damerau_levenshtein_distance("saturday", "sunday"),
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "Saturday",
        "saturday",
        normalized_damerau_levenshtein_distance("Saturday", "saturday"),
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "orange",
        "pumpkin",
        normalized_damerau_levenshtein_distance("orange", "pumpkin"),
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}".format(
        "gifts", "profit", normalized_damerau_levenshtein_distance("gifts", "profit")
    )
)
print(
    "normalized_damerau_levenshtein_distance('{}', '{}') = {}  # unicode example\n".format(
        "Sjöstedt",
        "Sjostedt",
        normalized_damerau_levenshtein_distance("Sjöstedt", "Sjostedt"),
    )
)  # unicode example

print("# edit distances for a single sequence against an array of sequences")
array = np.array(
    ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
)
print(
    "damerau_levenshtein_distance_ndarray('{}', np.array({})) = {}".format(
        "Saturday", array, damerau_levenshtein_distance_ndarray("Saturday", array)
    )
)
print(
    "normalized_damerau_levenshtein_distance_ndarray('{}', np.array({})) = {}\n".format(
        "Saturday",
        array,
        normalized_damerau_levenshtein_distance_ndarray("Saturday", array),
    )
)

print(
    "# normalized edit distances for a single sequence against an array of sequences - unicode"
)
array = np.array(["Sjöstedt", "Sjostedt", "Söstedt", "Sjöedt"])
print(
    "damerau_levenshtein_distance_ndarray('{}', np.array({})) = {}".format(
        "Sjöstedt", array, damerau_levenshtein_distance_ndarray("Sjöstedt", array)
    )
)
print(
    "normalized_damerau_levenshtein_distance_ndarray('{}', np.array({})) = {}\n".format(
        "Sjöstedt",
        array,
        normalized_damerau_levenshtein_distance_ndarray("Sjöstedt", array),
    )
)

# random words will be comprised of ascii letters, numbers, and spaces
print("# performance testing:")
chars = string.ascii_letters + string.digits + " "
word1 = "".join(
    [random.choice(chars) for i in range(30)]
)  # generate a random string of characters of length 30
word2 = "".join([random.choice(chars) for i in range(30)])  # and another
print(
    """\
timeit.timeit("damerau_levenshtein_distance('{}', '{}')", 
'from pyxdameraulevenshtein import damerau_levenshtein_distance', 
number=500000)
= {} seconds""".format(
        word1,
        word2,
        timeit.timeit(
            "damerau_levenshtein_distance('{}', '{}')".format(word1, word2),
            "from pyxdameraulevenshtein import damerau_levenshtein_distance",
            number=500000,
        ),
    )
)
print(
    """\
timeit.timeit("damerau_levenshtein_distance('{}', '{}')", 
'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000)
= {} seconds  # short-circuit makes this faster""".format(
        word1,
        word1,
        timeit.timeit(
            "damerau_levenshtein_distance('{}', '{}')".format(word1, word1),
            "from pyxdameraulevenshtein import damerau_levenshtein_distance",
            number=500000,
        ),
    )
)
