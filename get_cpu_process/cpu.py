#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/


import argparse
from get_cpu_process import get_pid, get_process_run_time, is_running, ProcessNotFound


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple CPU related script written by Zac the Wise utilising psutil"
    )

    # set arguments
    parser.add_argument(
        "--get-pid", action="store_true", help="returns PID of process name"
    )
    parser.add_argument(
        "--run-time", action="store_true", help="returns run time of process name"
    )
    parser.add_argument(
        "process_name", help="when used alone, returns True if process is running"
    )

    # parse args
    args = parser.parse_args()

    try:
        if args.get_pid:
            print(get_pid(provided_process_name=args.process_name))

        elif args.run_time:
            print(get_process_run_time(provided_process_name=args.process_name))

        elif args.process_name:
            print(is_running(provided_process_name=args.process_name))

        else:
            parser.print_help()

    except ProcessNotFound as e:
        print(str(e))
