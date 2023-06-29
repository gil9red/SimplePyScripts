#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import json

# pip install peewee
from peewee import *


db = SqliteDatabase("persons.sqlite", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    birthday = DateField()


class Pet(BaseModel):
    owner = ForeignKeyField(Person, backref="pets")
    name = CharField()
    animal_type = CharField()


db.connect()
db.create_tables([Person, Pet])

for person_data in json.load(open("persons.json", encoding="utf-8")):
    birthday = dt.datetime.strptime(person_data["birthday"], "%Y-%M-%d")
    person, _ = Person.get_or_create(name=person_data["name"], birthday=birthday)

    for pet in person_data["pets"]:
        Pet.get_or_create(
            owner=person, name=pet["name"], animal_type=pet["animal_type"]
        )


for person in Person.select():
    print(f"{person.name} ({person.birthday}). Pets: {person.pets.count()}")

    for pet in person.pets:
        print(f"    {pet.name} ({pet.animal_type}). Owner: {pet.owner.name}")

    print()

# Bob (1960-01-15). Pets: 1
#     Kitty (cat). Owner: Bob
#
# Grandma (1935-01-01). Pets: 0
#
# Herb (1950-01-05). Pets: 3
#     Fido (dog). Owner: Herb
#     Mittens (cat). Owner: Herb
#     Mittens Jr (cat). Owner: Herb
