import itertools

# Use an iterator version of xrange whether it's Python 3 or 2
try:
    irange = xrange
except:
    irange = range

tuplify = lambda gen: lambda *args, **kwargs: tuple(gen(*args, **kwargs))
chop_generator = lambda n: lambda gen: lambda *args, **kwargs: itertools.islice(gen(*args, **kwargs), n)

# functions for working with (score, probability tuples)
tuple_max = lambda tuples: max(tuples, key=lambda x: x[0])[0]
tuple_min = lambda tuples: min(tuples, key=lambda x: x[0])[0]
tuple_weighted_average = \
    lambda tuples: sum(
        score * probability
        for score, probability in tuples
    ) / sum(probability for score, probability in tuples)


def tuple_not_implemented(_):
    raise Exception("Score aggregation function not chosen")
