#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Decorator — Декоратор
# SOURCE: https://ru.wikipedia.org/wiki/Декоратор_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/decorator


class Notifier:
    def send(self, message: str) -> None:
        print(f'[Email] Send "{message}".')


class BaseDecorator(Notifier):
    def __init__(self, notifier: Notifier) -> None:
        self._wrapped = notifier


class SMSDecorator(BaseDecorator):
    def send(self, message: str) -> None:
        self._wrapped.send(message)

        print(f'[SMS] send "{message}".')


class FacebookDecorator(BaseDecorator):
    def send(self, message: str) -> None:
        self._wrapped.send(message)

        print(f'[Facebook] send "{message}".')


class SlackDecorator(BaseDecorator):
    def send(self, message: str) -> None:
        self._wrapped.send(message)

        print(f'[Slack] send "{message}".')


class Application:
    def __init__(self) -> None:
        self._notifier: Notifier = None

    def set_notifier(self, notifier: Notifier) -> None:
        self._notifier = notifier

    def about_alert(self) -> None:
        if self._notifier:
            self._notifier.send("Alert!")


if __name__ == "__main__":
    sms_enabled = True
    facebook_enabled = False
    slack_enabled = True

    notifier = Notifier()
    if sms_enabled:
        notifier = SMSDecorator(notifier)

    if facebook_enabled:
        notifier = FacebookDecorator(notifier)

    if slack_enabled:
        notifier = SlackDecorator(notifier)

    app = Application()
    app.set_notifier(notifier)

    app.about_alert()
    # [Email] Send "Alert!".
    # [SMS] send "Alert!".
    # [Slack] send "Alert!".

    print()

    notifier = Notifier()
    notifier.send("Test!")
    # [Email] Send "Test!".

    print()

    notifier = SMSDecorator(notifier)
    notifier = FacebookDecorator(notifier)
    notifier = SlackDecorator(notifier)
    notifier.send("Test!")
    # [Email] Send "Test!".
    # [SMS] send "Test!".
    # [Facebook] send "Test!".
    # [Slack] send "Test!".
