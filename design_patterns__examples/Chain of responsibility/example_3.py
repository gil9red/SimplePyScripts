#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Chain of responsibility — Цепочка обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей
# SOURCE: https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern#Python_Example


"""
Chain of responsibility pattern example.
"""

from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import List


class LogLevel(IntEnum):
    """
    Log Levels Enum.
    """

    NONE = auto()
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()
    FUNCTIONAL_MESSAGE = auto()
    FUNCTIONAL_ERROR = auto()
    ALL = auto()


class Logger(ABC):
    """
    Abstract handler in chain of responsibility pattern.
    """

    def __init__(self, levels: List[LogLevel]) -> None:
        """
        Initialize new logger

        Args:
            levels (List[LogLevel]): List of log levels.
        """

        self._next = None
        self._log_levels = list(levels)

    def set_next(self, next_logger: "Logger") -> "Logger":
        """
        Set next responsible logger in the chain.

        Args:
            next_logger (Logger): Next responsible logger.

        Returns:
            Logger: Next responsible logger.
        """
        self._next = next_logger
        return self._next

    def message(self, msg: str, severity: LogLevel) -> None:
        """
        Message writer handler.

        Args:
            msg (str): Message string.
            severity (LogLevel): Severity of message as log level enum.
        """
        if LogLevel.ALL in self._log_levels or severity in self._log_levels:
            self.write_message(msg)

        if self._next is not None:
            self._next.message(msg, severity)

    @abstractmethod
    def write_message(self, msg: str):
        """
        Abstract method to write a message.

        Args:
            msg (str): Message string.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("You should implement this method.")


class ConsoleLogger(Logger):
    def write_message(self, msg: str) -> None:
        """
        Overrides parent's abstract method to write to console.

        Args:
            msg (str): Message string.
        """
        print("Writing to console:", msg)


class EmailLogger(Logger):
    """
    Overrides parent's abstract method to send an email.

    Args:
        msg (str): Message string.
    """

    def write_message(self, msg: str) -> None:
        print("Sending via email:", msg)


class FileLogger(Logger):
    """
    Overrides parent's abstract method to write a file.

    Args:
        msg (str): Message string.
    """

    def write_message(self, msg: str) -> None:
        print("Writing to log file:", msg)


def main() -> None:
    """
    Building the chain of responsibility.
    """
    logger = ConsoleLogger([LogLevel.ALL])
    email_logger = logger.set_next(
        EmailLogger([LogLevel.FUNCTIONAL_MESSAGE, LogLevel.FUNCTIONAL_ERROR])
    )
    # As we don't need to use file logger instance anywhere later
    # We will not set any value for it.
    email_logger.set_next(
        FileLogger([LogLevel.WARNING, LogLevel.ERROR])
    )

    # ConsoleLogger will handle this part of code since the message
    # has a log level of all
    logger.message("Entering function ProcessOrder().", LogLevel.DEBUG)
    logger.message("Order record retrieved.", LogLevel.INFO)

    # ConsoleLogger and FileLogger will handle this part since file logger
    # implements WARNING and ERROR
    logger.message(
        "Customer Address details missing in Branch DataBase.",
        LogLevel.WARNING
    )
    logger.message(
        "Customer Address details missing in Organization DataBase.",
        LogLevel.ERROR
    )

    # ConsoleLogger and EmailLogger will handle this part as they implement
    # functional error
    logger.message(
        "Unable to Process Order ORD1 Dated D1 for customer C1.",
        LogLevel.FUNCTIONAL_ERROR
    )
    logger.message("OrderDispatched.", LogLevel.FUNCTIONAL_MESSAGE)


if __name__ == "__main__":
    main()
