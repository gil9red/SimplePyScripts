#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/33117579/5909792


import socket


DEFAULT_HOST: str = "8.8.8.8"
DEFAULT_PORT: int = 53
DEFAULT_TIMEOUT: int = 3


def check_internet(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: int = DEFAULT_TIMEOUT,
) -> bool:
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        return True
    except socket.error as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser(
        description="Check internet",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="Host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port",
    )
    parser.add_argument(
        "--network_timeout_secs",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Network timeout in seconds",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=3,
        help="Attempts to check",
    )
    parser.add_argument(
        "--delay_between_attempts_secs",
        type=int,
        default=30,
        help="Delay between attempts in seconds",
    )

    args = parser.parse_args()

    for attempt in range(args.attempts):
        prefix: str = f"[{attempt + 1}] "

        print(f"{prefix}Check internet")
        result: bool = check_internet(
            host=args.host,
            port=args.port,
            timeout=args.network_timeout_secs,
        )
        print(f"{prefix}Result: {result}")
        if result:
            break

        delay: int = args.delay_between_attempts_secs

        print(f"{prefix}The next attempt through {delay} seconds\n")
        time.sleep(delay)
