#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install email-validator
from email_validator import validate_email, EmailNotValidError


emails = [
    "my+address@mydomain.tld",
    "мой-адрес@mail.ru",
]
is_new_account = True  # False for login pages

for email in emails:
    try:
        # Check that the email address is valid.
        validation = validate_email(email, check_deliverability=is_new_account)

        # Take the normalized form of the email address
        # for all logic beyond this point (especially
        # before going to a database query where equality
        # may not take into account Unicode normalization).
        email = validation.email

    except EmailNotValidError as e:
        # Email is not valid.
        # The exception message is human-readable.
        print(f'{email!r}, error: {e!r}')
        # 'my+address@mydomain.tld', error: EmailUndeliverableError('The domain name mydomain.tld does not exist.')

    print(email)
"""
my+address@mydomain.tld
мой-адрес@mail.ru
"""

print()

is_new_account = False
for email in emails:
    validation = validate_email(email, check_deliverability=is_new_account)
    print(validation.email)
"""
my+address@mydomain.tld
мой-адрес@mail.ru
"""
