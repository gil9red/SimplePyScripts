#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/joke2k/faker


# pip install Faker
from faker import Faker


fake = Faker()

for _ in range(10):
    print(fake.name())

print("\n")

# With locale:
fake = Faker("ru_RU")
for _ in range(10):
    print(fake.name())
