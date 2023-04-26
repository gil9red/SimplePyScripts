__author__ = "ipetrash"


def create_massive(rows, cols, init_value):
    return [[init_value for c in range(cols)] for r in range(rows)]


def create_massive_2(rows, cols, init_value):
    massive = []
    for r in range(rows):
        massive.append([])

        for c in range(cols):
            massive[r].append(init_value)

    return massive


if __name__ == "__main__":
    rows = 5
    cols = 3
    massive = create_massive(rows, cols, None)
    massive_2 = create_massive_2(rows, cols, 1)

    print(massive)
    print(massive_2)
