# coding=utf-8

__author__ = 'ipetrash'


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
    return "INSERT INTO %s (%s) VALUES (%s)" % (table, ', '.join(columns), ', '.join(values))


def say_hello(word="World", spl="!"):
    print("Hello, " + word + spl)


if __name__ == '__main__':
    print(my_sum(1, 2, 3, 4))
    my_print(a=2, b=3, c="Foo")
    print(sql_insert("Users", login="TestUser", pas=123))
    print(sql_insert("Users", login="Vasya", pas=0123, sex="male"))
    say_hello()
    say_hello("Py")
    say_hello(spl="?")
    say_hello(spl="?!", word="man")
