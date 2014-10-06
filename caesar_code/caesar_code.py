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


if __name__ == '__main__':
    print(caesar_code("Hello World!", shift=2))
    print(caesar_code("Hello World!", shift=-4))
    print(caesar_code("Hello World!", shift=26))
    print(caesar_code("Hello World!", shift=50))
    print(caesar_code("Hello World!", shift=78))