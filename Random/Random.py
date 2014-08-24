__author__ = 'ipetrash'

import random

if __name__ == '__main__':
    direction = ["up", 'down', 'left', 'right']
    for i in range(5):
        print("Directions: %s, random direction = %s" % (direction, random.choice(direction)))

    print("random: %s" % random.random())  # rand float number
    print("randrange(5): %s" % random.randrange(5))  # rand int number
    print("randrange(0, 10): %s" % random.randrange(0, 10))  # rand int number
    print("uniform(1, 10): %s" % random.uniform(1, 10))  # rand float number

    print("Directions: %s" % direction)
    random.shuffle(direction)  # shuffle list
    print("Shuffle directions: %s" % direction)

    print(random.sample(direction, 2))  # select two element