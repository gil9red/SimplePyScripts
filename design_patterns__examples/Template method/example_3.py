#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: Design Patterns: Template method — Шаблонный метод
# SOURCE: https://ru.wikipedia.org/wiki/Шаблонный_метод_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/template-method/java/example


import time
import sys

from abc import ABC, abstractmethod


# Базовый класс социальной сети.
class Network(ABC):
    user_name: str
    password: str
    
    # Публикация данных в любой сети.
    def post(self, message: str) -> bool:
        # Проверка данных пользователя перед постом в соцсеть. Каждая сеть для
        # проверки использует разные методы.
        if self.log_in(self.user_name, self.password):
            # Отправка данных.
            result = self.send_data(message.encode())
            self.log_out()
            return result
        
        return False

    @abstractmethod
    def log_in(self, user_name: str, password: str) -> bool:
        pass

    @abstractmethod
    def send_data(self, data: bytes) -> bool:
        pass

    @abstractmethod
    def log_out(self):
        pass


# Класс социальной сети.
class Facebook(Network):
    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    def log_in(self, user_name: str, password: str) -> bool:
        print("\nChecking user's parameters")
        print("Name: " + self.user_name)
        print("Password: " + ('*' * len(self.password)), end='')

        self._simulate_network_latency()
        print("\n\nlog_in success on Facebook")
        return True

    def send_data(self, data: bytes) -> bool:
        message_posted = True
        if message_posted:
            print("Message: '" + data.decode() + "' was posted on Facebook")
            return True

        return False

    def log_out(self):
        print("User: '" + self.user_name + "' was logged out from Facebook")

    def _simulate_network_latency(self):
        print()

        try:
            i = 0
            while i < 10:
                print(".", end='')
                time.sleep(0.5)
                i += 1
            
        except Exception as e:
            print(e)


# Класс социальной сети.
class Twitter(Network):
    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    def log_in(self, user_name: str, password: str) -> bool:
        print("\nChecking user's parameters")
        print("Name: " + self.user_name)
        print("Password: " + ('*' * len(self.password)), end='')
        
        self._simulate_network_latency()
        print("\n\nlog_in success on Twitter")
        return True

    def send_data(self, data: bytes) -> bool:
        message_posted = True
        if message_posted:
            print("Message: '" + data.decode() + "' was posted on Twitter")
            return True

        return False

    def log_out(self):
        print("User: '" + self.user_name + "' was logged out from Twitter")

    def _simulate_network_latency(self):
        print()

        try:
            i = 0
            while i < 10:
                print(".", end='')
                time.sleep(0.5)
                i += 1

        except Exception as e:
            print(e)
        

if __name__ == '__main__':
    user_name = input("Input user name: ")
    password = input("Input password: ")

    # Вводим сообщение.
    message = input("Input message: ")

    choice = input("\nChoose social network for posting message.\n1 - Facebook\n2 - Twitter\n")
    network = None

    # Создаем сетевые объекты и публикуем пост.
    if choice == "1":
        network = Facebook(user_name, password)

    elif choice == "2":
        network = Twitter(user_name, password)

    else:
        print('Unknown network!')
        sys.exit()
    
    network.post(message)
