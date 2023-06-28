#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/questions/929442/


import tkinter as tk


alphabet = "abcdefghijklmnopqrstuvwxyz"


def on_selecting_file():
    pass


def on_change_symbols():
    pass


def on_window_deleted():
    print("Window closed")
    root.quit()


root = tk.Tk()
root.title("Example")
root.geometry("400x550+300+300")
root.protocol("WM_DELETE_WINDOW", on_window_deleted)

select_file_button = tk.Button(text="Select file", command=on_selecting_file)
select_file_button.place(relx=0.5, y=10)

change_letters_button = tk.Button(text="Change letters", command=on_change_symbols)
change_letters_button.place(relx=0.5, y=500)

pos = 0
x = 50
y = 50

try:
    for i in range(3):
        for j in range(9):
            letter = alphabet[pos]

            label = tk.Label(text=letter)
            label.place(x=x, y=y)

            entry = tk.Entry()
            entry.place(x=x + 30, y=y, width=30)

            globals()["label_" + letter] = label
            globals()["letter_" + letter] = entry

            pos += 1
            y += 50

        y = 50
        x += 100

# For quit from loops
except IndexError:
    pass

print(repr(label_a), repr(label_b), repr(label_c))
print(repr(letter_a), repr(letter_b), repr(letter_c))
# <tkinter.Label object .!label> <tkinter.Label object .!label2> <tkinter.Label object .!label3>
# <tkinter.Entry object .!entry> <tkinter.Entry object .!entry2> <tkinter.Entry object .!entry3>

root.mainloop()
