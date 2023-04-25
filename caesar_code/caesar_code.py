__author__ = "ipetrash"


"""Реализация алгоритма Код Цезаря."""


import typing
from string import ascii_lowercase, ascii_uppercase


ru_lowercase = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ru_uppercase = ru_lowercase.upper()

alphabet_list = [
    ascii_lowercase,
    ascii_uppercase,
    ru_lowercase,
    ru_uppercase,

    # Грузинский язык
    "აბგდევზთიკლმნოპჟრსტჳუფქღყშჩცძწჭხჴჯჰ",
]


def get_alp_by_char(char: str) -> typing.Optional[list]:
    for alphabet in alphabet_list:
        if char in alphabet:
            return alphabet

    return None


def caesar_code(text: str, shift: int) -> str:
    """Функция принимает текстовую строку и возвращает, новую строку
    символы которой сдвинуты по алфавиту."""

    shift_text = ""

    for c in text:
        alphabet = get_alp_by_char(c)
        if alphabet is None:
            shift_text += c
            continue

        i = (alphabet.index(c) + shift) % len(alphabet)
        shift_text += alphabet[i]

    return shift_text


if __name__ == "__main__":
    text = "Hello World!"
    print(caesar_code(text, shift=0))
    print(caesar_code(text, shift=2))
    print(caesar_code(text, shift=-4))
    print(caesar_code(text, shift=26))
    print(caesar_code(text, shift=50))
    print(caesar_code(text, shift=78))

    assert caesar_code(text, shift=0) == text
    assert caesar_code(text, shift=2) == "Jgnnq Yqtnf!"
    assert caesar_code(text, shift=-4) == "Dahhk Sknhz!"
    assert caesar_code(text, shift=26) == text
    assert caesar_code(text, shift=50) == "Fcjjm Umpjb!"
    assert caesar_code(text, shift=78) == text

    print()

    text = "Привет мир!"
    print(caesar_code(text, shift=0))
    print(caesar_code(text, shift=2))
    print(caesar_code(text, shift=-4))
    print(caesar_code(text, shift=33))
    print(caesar_code(text, shift=50))
    print(caesar_code(text, shift=99))

    assert caesar_code(text, shift=0) == text
    assert caesar_code(text, shift=2) == "Сткджф окт!"
    assert caesar_code(text, shift=-4) == "Лмеюбо ием!"
    assert caesar_code(text, shift=33) == text
    assert caesar_code(text, shift=50) == "Абщтхг эщб!"
    assert caesar_code(text, shift=99) == text

    print()
    text = "Hello мир!"
    print(caesar_code(text, shift=0))
    print(caesar_code(text, shift=2))
    print(caesar_code(text, shift=-4))

    assert caesar_code(text, shift=0) == text
    assert caesar_code(text, shift=2) == "Jgnnq окт!"
    assert caesar_code(text, shift=-4) == "Dahhk ием!"

    print()
    text = "გამარჯობა მსოფლიოში!"
    print(caesar_code(text, shift=0))
    print(caesar_code(text, shift=2))
    print(caesar_code(text, shift=-4))

    assert caesar_code(text, shift=0) == text
    assert caesar_code(text, shift=2) == "ეგოგტაჟდგ ოჳჟღნლჟცლ!"
    assert caesar_code(text, shift=-4) == "ჯხთხნწკჴხ თოკსზეკფე!"

    # Hint: see shift=23
    print()
    print()
    TEXT = "VWDQ LV QRW ZKDW KH VHHPV"
    for i in range(len(ascii_uppercase)):
        print(i, caesar_code(TEXT, i))
