#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


while True:
    oper = input("Enter 'add', 'substract', 'multiply', 'divide', 'quit', 'power': ")
    if oper == "quit":
        break

    try:
        if oper == "add":
            x = int(input("Enter 1st num: "))
            y = int(input("Enter 2nd num: "))
            print(x + y)
        elif oper == "substract":
            x = int(input("Enter 1st num: "))
            y = int(input("Enter 2nd num: "))
            print(x - y)
        elif oper == "multiply":
            x = int(input("Enter 1st num: "))
            y = int(input("Enter 2nd num: "))
            print(x * y)
        elif oper == "divide":
            x = int(input("Enter 1st num: "))
            y = int(input("Enter 2nd num: "))
            print(x / y)
        elif oper == "power":
            x = int(input("Enter the base: "))
            y = int(input("Enter the exponent: "))
            print(x**y)
        else:
            print("Unknown command!")

    except ValueError:
        print("Invalid value!")

print("Finish")
