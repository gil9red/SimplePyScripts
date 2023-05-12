__author__ = "ipetrash"


def fibo_1(n):
    f = [0, 1]
    for i in range(2, n + 1):
        f.append(f[i - 1] + f[i - 2])
    print(f)


def fibo_2(n):
    a, b = 0, 1
    print(a, b, end=" ")
    for i in range(2, n + 1):
        a, b = b, a + b
        print(b, end=" ")


if __name__ == "__main__":
    # Fibo / Фибоначчи
    n = 10
    fibo_1(n)
    print()
    fibo_2(n)
