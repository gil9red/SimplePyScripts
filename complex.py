__author__ = "ipetrash"


if __name__ == "__main__":
    # Комплексные числа (complex)
    # В Python встроены также и комплексные числа:

    x = complex(1, 2)
    print(x)

    y = complex(3, 4)
    print(y)

    z = x + y
    print(x)
    print(z)

    z = x * y
    print(z)

    z = x / y
    print(z)
    print(x.conjugate())  # Сопряжённое число
    print(x.imag)  # Мнимая часть
    print(x.real)  # Действительная часть
    # print ( x > y ) # Комплексные числа нельзя сравнить
    print(x == y)  # Но можно проверить на равенство
    print(abs(3 + 4j))  # Модуль комплексного числа
    print(pow(3 + 4j, 2))  # Возведение в степень

    # Также для работы с комплексными числами используется также модуль cmath .
