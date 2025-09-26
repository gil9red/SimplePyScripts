__author__ = "ipetrash"


# TODO: больше примеров
# https://docs.python.org/3.4/library/datetime.html
# http://pythonworld.ru/moduli/modul-datetime.html


from datetime import datetime, date, timedelta


# Dates are easily constructed and formatted
now = datetime.today()
print(now)
print(now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B."))

# Dates support calendar arithmetic
birthday: date = datetime(year=1964, month=7, day=31)
age: timedelta = now - birthday
print(age.days)

print()

now = date.today()
print(now)
print(now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B."))

# Dates support calendar arithmetic
birthday: date = date(year=1964, month=7, day=31)
age: timedelta = now - birthday
print(age.days)
