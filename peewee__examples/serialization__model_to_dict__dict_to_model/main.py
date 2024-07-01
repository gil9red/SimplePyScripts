#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt

# pip install peewee
from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField

from playhouse.shortcuts import model_to_dict, dict_to_model


db = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    birthday = DateField()

    def __str__(self):
        return (
            f"Person(id={self.id} name={self.name!r} birthday={self.birthday} "
            f'pets={", ".join(p.name for p in self.pets)!r})'
        )


class Pet(BaseModel):
    owner = ForeignKeyField(Person, backref="pets")
    name = CharField()
    animal_type = CharField()

    def __str__(self):
        return f"Pet(id={self.id} name={self.name!r} owner={self.owner.name!r} self.animal_type={self.animal_type!r})"


db.connect()
db.create_tables([Person, Pet])

person = Person.create(name="Ivan", birthday=dt.date.today())

Pet.create(owner=person, name="Oval", animal_type="Dog")
Pet.create(owner=person, name="Bortik", animal_type="Cat")

print(person)
# Person(id=1 name='Ivan' birthday=2020-01-09 pets='Oval, Bortik')

print()

data_backrefs_false = model_to_dict(person)
print(type(data_backrefs_false), data_backrefs_false)
# <class 'dict'> {'id': 1, 'name': 'Ivan', 'birthday': datetime.date(2020, 1, 9)}

data_backrefs_true = model_to_dict(person, backrefs=True)
print(type(data_backrefs_true), data_backrefs_true)
# <class 'dict'> {'id': 1, 'name': 'Ivan', 'birthday': datetime.date(2020, 1, 9),
# 'pets': [{'id': 1, 'name': 'Oval', 'animal_type': 'Dog'}, {'id': 2, 'name': 'Bortik', 'animal_type': 'Cat'}]}

print()

# Create another database and import this
db = SqliteDatabase("persons.sqlite", pragmas={"foreign_keys": 1})
Person._meta.database = db
Pet._meta.database = db
db.connect()
db.create_tables([Person, Pet])

Pet.truncate_table()
Person.truncate_table()
#

person = dict_to_model(Person, data_backrefs_false)
print(person)
print(list(person.pets))
print(list(Pet.select()))
# Person(id=1 name='Ivan' birthday=2020-01-09 pets='')
# []
# []

print()

person = dict_to_model(Person, data_backrefs_true)
print(person)
person.save(force_insert=True)  # Must-have .save( and force_insert=True
print(list(person.pets))
for p in person.pets:
    p.save(force_insert=True)
print(list(Pet.select()))
# Person(id=1 name='Ivan' birthday=2020-01-09 pets='Oval, Bortik')
# [<Pet: Pet(id=1 name='Oval' owner='Ivan' self.animal_type='Dog')>, <Pet: Pet(id=2 name='Bortik' owner='Ivan' self.animal_type='Cat')>]
# [<Pet: Pet(id=1 name='Oval' owner='Ivan' self.animal_type='Dog')>, <Pet: Pet(id=2 name='Bortik' owner='Ivan' self.animal_type='Cat')>]
