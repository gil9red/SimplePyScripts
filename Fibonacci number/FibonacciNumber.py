__author__ = 'ipetrash'

def fibo_1(n):
    f = [0, 1]
    for i in range(2, n + 1):
        f.append(f[i-1] + f[i-2])
    print(f)


def fibo_2(n):
    a = 0
    b = 1
    print(a, b, end=' ')
    for i in range(2, n + 1):
        c = a + b
        a, b = b, c
        print(c, end=' ')


if __name__ == '__main__':
    # Fibo / Фибоначчи
    n = 10
    fibo_1(n)
    fibo_2(n)