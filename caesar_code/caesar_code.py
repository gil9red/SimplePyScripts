__author__ = 'ipetrash'


"""Скрипт реализует простейшую реализацию алгоритма Код Цезаря."""


def caesar_code(text, shift):
    """Функция принимает текстовую строку и возвращает, новую строку
    символы которой сдвинуты по алфавиту."""

    alp = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    new_t = ''
    for c in text.lower():
        if c in alp:
            i = (alp.index(c) + shift) % len(alp)
            new_t += alp[i]
        else:
            new_t += c
    return new_t


from string import ascii_uppercase


def shift(text, num):
    shift_text = ''

    for c in text:
        if c not in ascii_uppercase:
            shift_text += c
            continue

        i = (ascii_uppercase.index(c) + num) % len(ascii_uppercase)
        shift_text += ascii_uppercase[i]

    return shift_text


if __name__ == '__main__':
    print(caesar_code("Hello World!", shift=2))
    print(caesar_code("Hello World!", shift=-4))
    print(caesar_code("Hello World!", shift=26))
    print(caesar_code("Hello World!", shift=50))
    print(caesar_code("Hello World!", shift=78))

    print()

    TEXT = 'VWDQ LV QRW ZKDW KH VHHPV'

    for i in range(len(ascii_uppercase)):
        print(i, shift(TEXT, i))
