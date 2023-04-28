__author__ = "ipetrash"


# TODO: больше примеров
# https://docs.python.org/3.4/library/datetime.html
# http://pythonworld.ru/moduli/modul-datetime.html


from datetime import date


if __name__ == "__main__":
    # Dates are easily constructed and formatted
    now = date.today()
    print(now)
    print(now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B."))

    # Dates support calendar arithmetic
    birthday = date(1964, 7, 31)
    age = now - birthday
    print(age.days)
