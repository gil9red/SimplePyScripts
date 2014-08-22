__author__ = 'ipetrash'

# Guess the number / Угадай число
import random

if __name__ == '__main__':
    max = int(input("Input max: "))
    print("Random number (x): from %d to %d" % (1, max))
    number = random.randrange(1, max + 1)
    user_choice = -1
    range_min = range_max = "?"

    while True:
        print("\n%s < x < %s" % (range_min, range_max))
        user_choice = int(input("Input number: "))
        if number > user_choice:
            if range_min == "?":
                range_min = user_choice
            if user_choice > range_min:
                range_min = user_choice
            print("x > %d" % user_choice)

        elif number < user_choice:
            if range_max == "?":
                range_max = user_choice
            if user_choice < range_max:
                range_max = user_choice
            print("x < %d" % user_choice)

        elif number == user_choice:
            print("Congratulations! You guessed it!")
            break
