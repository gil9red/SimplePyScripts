#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Observer — Наблюдатель
# SOURCE: https://ru.wikipedia.org/wiki/Наблюдатель_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/observer/java/example


"""
В этом примере Наблюдатель используется для передачи событий между объектами текстового редактора. Всякий раз 
когда объект редактора меняет своё состояние, он оповещает своих наблюдателей. Объекты EmailNotificationListener и 
LogOpenListener следят за этими уведомлениями и выполняют полезную работу в ответ.

Классы подписчиков не связаны с классом редактора и могут быть повторно использованы в других приложениях если 
потребуется. Класс Editor зависит только от общего интерфейса подписчиков. Это позволяет добавлять новые типы 
подписчиков не меняя существующего кода редактора.
"""


from abc import ABC, abstractmethod
from typing import IO


class EventListener(ABC):
    @abstractmethod
    def update(self, event_type: str, file: IO):
        pass


class EventManager:
    def __init__(self, *operations):
        self.listeners: dict[str, list[EventListener]] = dict()

        for operation in operations:
            self.listeners[operation] = []

    def subscribe(self, event_type: str, listener: EventListener):
        items = self.listeners[event_type]
        items.append(listener)

    def unsubscribe(self, event_type: str, listener: EventListener):
        items = self.listeners[event_type]
        if listener in items:
            items.remove(listener)

    def notify(self, event_type: str, file: IO):
        items = self.listeners[event_type]
        for listener in items:
            listener.update(event_type, file)


class Editor:
    def __init__(self):
        self.file: IO = None
        self.events = EventManager("open", "save")

    def open_file(self, file_path: str):
        self.file = open(file_path, "w", encoding="utf-8")
        self.events.notify("open", self.file)

    def save_file(self):
        if self.file and not self.file.closed:
            self.events.notify("save", self.file)
        else:
            raise Exception("Please open a file first.")


class EmailNotificationListener(EventListener):
    def __init__(self, email: str):
        self.email = email

    def update(self, event_type: str, file: IO):
        print(
            f"Email to {self.email}: Someone has performed {event_type} "
            f"operation with the following file: {file.name}"
        )


class LogOpenListener(EventListener):
    def __init__(self, file_name: str):
        # self.log: IO = open(file_name, encoding='utf-8')
        self.file_name = file_name

    def update(self, event_type: str, file: IO):
        # print(f"Save to log {self.log}: Someone has performed {event_type} "
        #       f"operation with the following file: {file.name}")
        print(
            f"Save to log {self.file_name}: Someone has performed {event_type} "
            f"operation with the following file: {file.name}"
        )


if __name__ == "__main__":
    editor = Editor()
    editor.events.subscribe("open", LogOpenListener("/path/to/log/file.txt"))
    editor.events.subscribe("save", EmailNotificationListener("admin@example.com"))

    try:
        editor.open_file("test.txt")
        editor.save_file()

    except Exception as e:
        print(e)
