#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/19719292/5909792


def is_user_admin():
    import os

    if os.name == 'nt':
        import ctypes
        try:
            # WARNING: requires Windows XP SP2 or higher!
            return bool(ctypes.windll.shell32.IsUserAnAdmin())

        except:
            import traceback
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False

    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0

    else:
        raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))


if __name__ == '__main__':
    print(is_user_admin())
