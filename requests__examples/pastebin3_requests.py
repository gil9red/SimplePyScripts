#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


class PastebinError(Exception):
    pass


class PastebinRequestError(PastebinError):
    pass


# TODO: docstring
# TODO: correct comments and strings: my bad english :(


PASTEBIN_API_VERSION = "3.1"

__API_LOGIN_URL = "http://pastebin.com/api/api_login.php"
__API_POST_URL = "http://pastebin.com/api/api_post.php"

# We have 3 valid values available which you can use with the 'api_paste_private' parameter:
__PRIVATE_VARIANTS = {"public": 0, "unlisted": 1, "private": 2}


def __send_post_request_by_pastebin(url, params):
    """

    :param url:
    :param params:
    :return:
    """

    rs = requests.post(url, data=params)

    if not rs.ok:
        raise PastebinRequestError("HTTP status code: " + str(rs.status_code))

    if rs.text.startswith("Bad API request"):
        raise PastebinRequestError(rs.text)

    return rs


def __send_api_post_request(params):
    return __send_post_request_by_pastebin(__API_POST_URL, params)


def api_user_key(dev_key, user_name, user_password):
    """

    :param dev_key:
    :param user_name:
    :param user_password:
    :return:
    """

    params = {
        "api_dev_key": dev_key,
        "api_user_name": user_name,
        "api_user_password": user_password,
    }

    rs = __send_post_request_by_pastebin(__API_LOGIN_URL, params)
    return rs.text


def user_pastes(dev_key, user_key, results_limit=50):
    """Listing Pastes Created By A User

    :param dev_key:
    :param user_key:
    :param results_limit:
    :return:
    """

    params = {
        "api_dev_key": dev_key,
        "api_user_key": user_key,
        "api_results_limit": results_limit,
        "api_option": "list",
    }

    rs = __send_api_post_request(params)
    return rs.text


def trending(dev_key):
    """Listing Trending Pastes

    :param dev_key:
    :return:
    """

    params = {
        "api_dev_key": dev_key,
        "api_option": "trends",
    }

    rs = __send_api_post_request(params)
    return rs.text


def paste(
    dev_key, code, user_key=None, name=None, format=None, private=None, expire_date=None
):
    """Creating A New Paste

    :param dev_key:
    :param code:
    :param user_key:
    :param name:
    :param format:
    :param private:
    :param expire_date:
    :return:
    """

    if private:
        private = __PRIVATE_VARIANTS.get(private.lower())

        if private == 2 and user_key is None:
            raise PastebinError(
                "Private paste only allowed in combination with api_user_key, "
                "as you have to be logged into your account to access the paste"
            )

    params = {
        "api_dev_key": dev_key,
        "api_option": "paste",
        "api_paste_code": code,
        "api_user_key": user_key,
        "api_paste_name": name,
        "api_paste_format": format,
        "api_paste_private": private,
        "api_paste_expire_date": expire_date,
    }

    rs = __send_api_post_request(params)
    return rs.text


def delete_paste(dev_key, user_key, paste_key) -> bool:
    """Deleting A Paste Created By A User

    :param dev_key:
    :param user_key:
    :param paste_key:
    :return:
    """

    params = {
        "api_dev_key": dev_key,
        "api_user_key": user_key,
        "api_paste_key": paste_key,
        "api_option": "delete",
    }

    rs = __send_api_post_request(params)
    if rs.text.startswith("Paste Removed"):
        return True

    return False


def user_details(dev_key, user_key):
    """Getting A Users Information And Settings

    :param dev_key:
    :param user_key:
    :return:
    """

    params = {
        "api_dev_key": dev_key,
        "api_user_key": user_key,
        "api_option": "userdetails",
    }

    rs = __send_api_post_request(params)
    return rs.text
