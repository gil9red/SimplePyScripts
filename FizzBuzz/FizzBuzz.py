__author__ = "ipetrash"


# EN:
# Write a program that displays a number from 1 to 100. In this case, instead of numbers that are
# multiples of three, the program should display the word «Fizz», but instead of multiples of five - the
# word «Buzz». If the number is a multiple and 3 and 5, the program should display the word «FizzBuzz»

# RU:
# Напишите программу, которая выводит на экран числа от 1 до 100. При этом вместо чисел, кратных трем, программа
# должна выводить слово «Fizz», а вместо чисел, кратных пяти — слово «Buzz». Если число кратно и 3, и 5,
# то программа должна выводить слово «FizzBuzz»


for num in range(1, 100 + 1):
    if num % 15 is 0:
        print("FizzBuzz")
    elif num % 3 is 0:
        print("Fizz")
    elif num % 5 is 0:
        print("Buzz")
    else:
        print(num)
