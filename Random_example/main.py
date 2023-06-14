__author__ = "ipetrash"


import random


direction = ["up", "down", "left", "right"]
for i in range(5):
    print(
        f"Directions: {direction}, random direction = {random.choice(direction)}"
    )

print(f"random: {random.random()}")  # rand float number
print(f"randrange(5): {random.randrange(5)}")  # rand int number
print(f"randrange(0, 10): {random.randrange(0, 10)}")  # rand int number
print(f"uniform(1, 10): {random.uniform(1, 10)}")  # rand float number

print(f"Directions: {direction}")
random.shuffle(direction)  # shuffle list
print(f"Shuffle directions: {direction}")

print(random.sample(direction, 2))  # select two element
