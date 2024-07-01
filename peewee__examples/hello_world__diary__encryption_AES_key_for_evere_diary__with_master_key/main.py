#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/coleifer/peewee/blob/afdf7b752dcadbf440faaa91a7fb0f403eac9a69/examples/diary.py


import datetime as dt
import hashlib
import sys

from getpass import getpass

# pip install peewee
from peewee import Model, SqliteDatabase, TextField, DateTimeField

sys.path.append("../hello_world__diary__encryption_all_in_one_AES")
from utils.security import CryptoAES, AuthenticationError
from utils.utils import shorten


db = SqliteDatabase("my_database.sqlite")


class BaseModel(Model):
    class Meta:
        database = db


# Password: 123
ENCRYPT_MASTER_KEY = "A665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3"
# OR:
# ENCRYPT_MASTER_KEY = None

if not ENCRYPT_MASTER_KEY:
    #
    # OR encrypted_key using password:
    #
    # Need password
    password = getpass()
    if not password:
        print("Required password!")
        sys.exit()

    ENCRYPT_MASTER_KEY = hashlib.sha256(bytes(password, "utf-8")).hexdigest().upper()


class Diary(BaseModel):
    encrypted_content = TextField()  # Содержимое будет шифровано ключом
    encrypted_key = TextField()  # Ключ будет шифрован мастер ключом
    created_date = DateTimeField(default=dt.datetime.now)

    @staticmethod
    def create_encrypted_content(content: str, master_key: str) -> "Diary":
        key = CryptoAES.get_random_key_hex()

        encrypted_content = CryptoAES(key).encrypt(content)
        encrypted_key = CryptoAES(master_key).encrypt(key)

        return Diary(
            encrypted_content=encrypted_content, encrypted_key=encrypted_key
        ).save()

    def get_content(self, master_key: str) -> str:
        try:
            # Расшифровываем ключ мастер ключом
            key = self.get_key(master_key)

            # Расшифровываем содержимое ключом
            return CryptoAES(key).decrypt(self.encrypted_content)

        except AuthenticationError as e:
            return f"ERROR: {e}"

    def get_key(self, master_key: str) -> str:
        try:
            # Расшифровываем ключ мастер ключом
            return CryptoAES(master_key).decrypt(self.encrypted_key)

        except AuthenticationError as e:
            return f"ERROR: {e}"

    @staticmethod
    def print_table(master_key: str = ENCRYPT_MASTER_KEY):
        """Print all diaries"""

        header_fmt = "{:<3}  | {:<50} | {:<50} | {:<50} | {:<50} | {:<19}"
        row_fmt = "#{id:<3} | {encrypted_content:<50} | {content:<50} | {encrypted_key:<50} | {key:<50} | {created_date:%d/%m/%Y %H:%M:%S}"

        print(
            header_fmt.format(
                "ID",
                "ENCRYPTED_CONTENT",
                "CONTENT",
                "ENCRYPTED_KEY",
                "KEY",
                "CREATED_DATE",
            )
        )

        for diary in Diary.select():
            print(
                row_fmt.format(
                    id=diary.id,
                    encrypted_content=shorten(diary.encrypted_content),
                    content=shorten(diary.get_content(master_key)),
                    encrypted_key=shorten(diary.encrypted_key),
                    key=shorten(diary.get_key(master_key)),
                    created_date=diary.created_date,
                )
            )

        print()


db.connect()
db.create_tables([Diary])


# Вызываем в первый раз, чтобы заполнить таблицу
if not Diary.select().count():
    Diary.create_encrypted_content(
        content="Hello World!", master_key=ENCRYPT_MASTER_KEY
    )
    Diary.create_encrypted_content(
        content="The quick brown fox jumps over the lazy dog.",
        master_key=ENCRYPT_MASTER_KEY,
    )


def add_diary(master_key: str = ENCRYPT_MASTER_KEY):
    """Add diary"""

    data = input("Enter your diary: ").strip()
    if data and input("Save diary? [Y/n] ") != "n":
        Diary.create_encrypted_content(content=data, master_key=master_key)
        print("Saved successfully.")
        print()


def view_diaries(master_key: str = ENCRYPT_MASTER_KEY):
    """View previous diaries"""

    query = Diary.select().order_by(Diary.created_date.desc())
    for diary in query:
        print()
        timestamp = diary.created_date.strftime("%d/%m/%Y %H:%M:%S")
        print(timestamp)
        print("=" * len(timestamp))
        print(diary.encrypted_content)
        print(diary.get_content(master_key))
        print()
        print("n) next diary")
        print("d) delete diary")
        print("q) return to main menu")
        action = input("Choice? (N/d/q) ").lower().strip()
        if action == "q":
            break
        elif action == "d":
            diary.delete_instance()
            break


MENU = {
    "a": add_diary,
    "v": view_diaries,
    "p": Diary.print_table,
}


def menu_loop():
    choice = None
    while choice != "q":
        for key, value in MENU.items():
            print("%s) %s" % (key, value.__doc__))
        choice = input("Action: ").lower().strip()
        if choice in MENU:
            MENU[choice]()


Diary.print_table(ENCRYPT_MASTER_KEY)

menu_loop()
