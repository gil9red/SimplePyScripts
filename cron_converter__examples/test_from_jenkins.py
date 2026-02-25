#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime
from unittest import TestCase

from cron_converter import Cron

from from_jenkins import do_convert


class Test(TestCase):
    def test_do_convert_every_15_minutes(self) -> None:
        # Every fifteen minutes
        cron = "H/15 * * * *"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2024-01-01T12:00:00", "2024-01-01T12:15:00", "2024-01-01T12:30:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_every_1_hours(self) -> None:
        cron = "H * * * *"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2024-01-01T12:00:00", "2024-01-01T13:00:00", "2024-01-01T14:00:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_every_8_hours(self) -> None:
        cron = "H */8 * * *"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-01-01T16:00:00",
            "2024-01-02T00:00:00",
            "2024-01-02T08:00:00",
            "2024-01-02T16:00:00",
            "2024-01-03T00:00:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_every_24_hours(self) -> None:
        cron = "H 0 * * *"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2024-01-02T00:00:00", "2024-01-03T00:00:00", "2024-01-04T00:00:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_hourly(self) -> None:
        cron = "@hourly"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2024-01-01T12:00:00", "2024-01-01T13:00:00", "2024-01-01T14:00:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_daily(self) -> None:
        cron = "@daily"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2024-01-02T00:00:00", "2024-01-03T00:00:00", "2024-01-04T00:00:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_midnight(self) -> None:
        cron = "@midnight"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-01-02T00:00:00",
            "2024-01-03T00:00:00",
            "2024-01-04T00:00:00",
            "2024-01-05T00:00:00",
            "2024-01-06T00:00:00",
            "2024-01-07T00:00:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_weekly(self) -> None:
        cron = "@weekly"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-01-07T00:00:00",
            "2024-01-14T00:00:00",
            "2024-01-21T00:00:00",
            "2024-01-28T00:00:00",
            "2024-02-04T00:00:00",
            "2024-02-11T00:00:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_monthly(self) -> None:
        cron = "@monthly"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-02-01T00:00:00",
            "2024-03-01T00:00:00",
            "2024-04-01T00:00:00",
            "2024-05-01T00:00:00",
            "2024-06-01T00:00:00",
            "2024-07-01T00:00:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_yearly(self) -> None:
        cron = "@yearly"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2025-01-01T00:00:00", "2026-01-01T00:00:00", "2027-01-01T00:00:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_annually(self) -> None:
        cron = "@annually"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = ["2025-01-01T00:00:00", "2026-01-01T00:00:00", "2027-01-01T00:00:00"]

        self.assertEqual(actual, expected)

    def test_do_convert_complex_1(self) -> None:
        # Every ten minutes in the first half of every hour
        cron = "H(0-29)/10 * * * *"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-01-01T12:00:00",
            "2024-01-01T12:10:00",
            "2024-01-01T12:20:00",
            "2024-01-01T13:00:00",
            "2024-01-01T13:10:00",
            "2024-01-01T13:20:00",
            "2024-01-01T14:00:00",
            "2024-01-01T14:10:00",
            "2024-01-01T14:20:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_complex_2(self) -> None:
        # Once every two hours at 45 minutes past the hour starting at 9:45 AM and finishing at 3:45 PM every weekday
        cron = "45 9-16/2 * * 1-5"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-04T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-01-04T13:45:00",
            "2024-01-04T15:45:00",
            "2024-01-05T09:45:00",
            "2024-01-05T11:45:00",
            "2024-01-05T13:45:00",
            "2024-01-05T15:45:00",
            "2024-01-08T09:45:00",
            "2024-01-08T11:45:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_complex_3(self) -> None:
        # Once in every two hour slot between 8 AM and 4 PM every weekday
        cron = "H H(8-15)/2 * * 1-5"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2024-01-04T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2024-01-04T12:00:00",
            "2024-01-04T14:00:00",
            "2024-01-05T08:00:00",
            "2024-01-05T10:00:00",
            "2024-01-05T12:00:00",
            "2024-01-05T14:00:00",
            "2024-01-08T08:00:00",
            "2024-01-08T10:00:00",
        ]

        self.assertEqual(actual, expected)

    def test_do_convert_complex_4(self) -> None:
        # Once a day on the 1st and 15th of every month except December
        cron = "H H 1,15 1-11 *"

        cron = do_convert(cron)

        cron_instance = Cron(cron)

        start_date_str = "2023-10-01T12:00:00"
        schedule = cron_instance.schedule(datetime.fromisoformat(start_date_str))

        actual: list[str] = [
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
            schedule.next().isoformat(),
        ]
        expected = [
            "2023-10-15T00:00:00",
            "2023-11-01T00:00:00",
            "2023-11-15T00:00:00",
            "2024-01-01T00:00:00",
            "2024-01-15T00:00:00",
            "2024-02-01T00:00:00",
            "2024-02-15T00:00:00",
            "2024-03-01T00:00:00",
        ]

        self.assertEqual(actual, expected)
