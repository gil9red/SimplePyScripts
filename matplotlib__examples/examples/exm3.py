__author__ = "ipetrash"


# Простой пример рисования графика

import pylab

if __name__ == "__main__":
    pylab.plot(range(1, 20), [i * i for i in range(1, 20)], "ro")
    # pylab.savefig('example.png')
    pylab.show()
