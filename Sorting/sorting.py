__author__ = "ipetrash"


# Sort / Сортировка
# https://wiki.python.org/moin/HowTo/Sorting


import random


l = [x for x in range(20)]
random.shuffle(l)
print("List: %s" % l)
l.sort()
print("Sorted list: %s" % l)
l.sort(reverse=True)
print("Reversed Sorted list: %s" % l)

print()
m = [x for x in range(20)]
random.shuffle(m)
print("Sorted list: %s" % sorted(m))
print("Reversed Sorted list: %s" % sorted(m, reverse=True))


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return "%s (%d)" % (self.name, self.age)


students = list()
students.append(Student("Вася", 15))
students.append(Student("Аня", 16))
students.append(Student("Петя", 14))
students.append(Student("Эдуарт", 25))
students.append(Student("Таня", 16))
students.append(Student("Саша", 15))
print(students)

students.sort(key=lambda x: x.age)  # Sorted by 'age'
print(students)

students.sort(key=lambda x: x.age, reverse=True)  # Sorted by 'age'
print(students)


students.sort(key=lambda x: x.name)  # Sorted by 'name'
print(students)


print()
words = ["he", "He", "Ab", "ab", "Cc", "cC"]
print(f"Words: {words}")
print("Sorting:")
print(sorted(words))
print(sorted(words, reverse=True))
print()

# Sorting insensitive
print("Sorting insensitive:")
# print(sorted(words, key=lambda x: x.lower()))
print(sorted(words, key=str.lower))

# print(sorted(words, key=lambda x: x.lower(), reverse=True))
print(sorted(words, key=str.lower, reverse=True))
