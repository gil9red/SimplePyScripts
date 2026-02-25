__author__ = "ipetrash"


def getprint(str="hello world!") -> None:
    print(str)


def decor(func):
    def wrapper(*args, **kwargs):
        print("1 begin: " + func.__name__)
        print(f"Args={args} kwargs={kwargs}")
        f = func(*args, **kwargs)
        print("2 end: " + func.__name__ + "\n")
        return f

    return wrapper


def predecor(w="W") -> None:
    print(w, end=": ")


getprint()
getprint("Py!")
print()
f = decor(getprint)
f()
f("Py!")


def rgb2hex(get_rgb_func):
    def wrapper(*args, **kwargs) -> str:
        r, g, b = get_rgb_func(*args, **kwargs)
        return f"#{r:02x}{g:02x}{b:02x}"

    return wrapper


class RGB:
    def __init__(self) -> None:
        self._r = 0xFF
        self._g = 0xFF
        self._b = 0xFF

    def getr(self):
        return self._r

    def setr(self, r) -> None:
        self._r = r

    r = property(getr, setr)

    def getg(self):
        return self._g

    def setg(self, g) -> None:
        self._g = g

    g = property(getg, setg)

    def getb(self):
        return self._b

    def setb(self, b) -> None:
        self._b = b

    b = property(getb, setb)

    def setrgb(self, r, g, b) -> None:
        self.r, self.g, self.b = r, g, b

    @rgb2hex
    def getrgb(self):
        return (self.r, self.g, self.b)


rgb = RGB()
print(f"rgb.r={rgb.r}")
rgb.setrgb(0xFF, 0x1, 0xFF)
print(f"rgb.getrgb(): {rgb.getrgb()}")
print()


@decor
def foo(a, b) -> None:
    print(f"{a} ^ {b} = {(a ** b)}")


foo(2, 3)
foo(b=3, a=2)
