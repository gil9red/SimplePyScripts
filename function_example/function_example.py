__author__ = "ipetrash"


def my_sum(*args):
    s = 0
    for arg in args:
        s += int(arg)
    return s


def my_print(**kwargs):
    for name, value in kwargs.items():
        print("%s=%s(%s)" % (name, value, type(value)))


def sql_insert(table, **kwargs):
    # Example: INSERT INTO users (login, pass) values('TestUser', '123456')
    columns = kwargs.keys()
    values = ["'%s'" % x for x in kwargs.values()]
    return "INSERT INTO %s (%s) VALUES (%s)" % (
        table,
        ", ".join(columns),
        ", ".join(values),
    )


def say_hello(word="World", spl="!"):
    print("Hello, " + word + spl)


def my_min(a, b):
    return min(a, b)


def my_max(a, b):
    return max(a, b)


def binary_operation(a, b, func):
    return func(a, b)


# http://pythonworld.ru/tipy-dannyx-v-python/vse-o-funkciyax-i-ix-argumentax.html

if __name__ == "__main__":
    print(my_sum(1, 2, 3, 4))
    my_print(a=2, b=3, c="Foo")
    print(sql_insert("Users", login="TestUser", pas=123))
    print(sql_insert("Users", login="Vasya", pas=123, sex="male"))
    say_hello()
    say_hello("Py")
    say_hello(spl="?")
    say_hello(spl="?!", word="man")

    print()

    a = 2
    b = 4
    print("1: %d" % binary_operation(a, b, my_min))
    print("2: %d" % binary_operation(a, b, my_max))
    print("3: %d" % binary_operation(a, b, min))
    print("4: %d" % binary_operation(a, b, max))
    print("5: %d" % binary_operation(a, b, lambda a, b: a * b))
    print("6: %d" % binary_operation(a, b, lambda a, b: a**b))

    print()

    lambda_sum = lambda a, b: a + b
    print(lambda_sum(1, 1))
    print(lambda_sum(1.1, 1.9))
    print(lambda_sum("a", "bc"))
    print(lambda_sum([1, 2], [3, 4]))

    print()

    print((lambda a, b: a**b)(2, 3))
    print((lambda a, b: a / b)(4, 2))
