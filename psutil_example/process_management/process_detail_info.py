#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: Need run as admin

# pip install psutil
import psutil


def print_info(pid):
    process = psutil.Process(pid)
    print("Process:", process)

    print("name:", process.name())
    print("as_dict:", process.as_dict())
    print("is_running:", process.is_running())

    print("exe:", process.exe())
    print("cwd:", process.cwd())
    print("cmdline:", process.cmdline())
    print("pid:", process.pid)
    print("ppid:", process.ppid())
    print("parent:", process.parent())
    print("children:", process.children())
    print("status:", process.status())
    print("username:", process.username())
    print("create_time:", process.create_time())

    # If POSIX:
    # print('uids:', process.uids())
    # print('gids:', process.gids())

    print("cpu_times:", process.cpu_times())
    print("cpu_percent:", process.cpu_percent(interval=1.0))
    print("cpu_affinity:", process.cpu_affinity())
    print("cpu_affinity:", process.cpu_affinity([0, 1]))

    # If Linux, FreeBSD, SunOS
    # print('cpu_num:', process.cpu_num())

    print("memory_info:", process.memory_info())
    print("memory_full_info:", process.memory_full_info())
    print("memory_percent:", process.memory_percent())
    print("memory_maps:", process.memory_maps())
    print("io_counters:", process.io_counters())
    print("open_files:", process.open_files())
    print("connections:", process.connections())
    print("num_threads:", process.num_threads())

    # If POSIX
    # print('num_fds:', process.num_fds())

    print("threads:", process.threads())
    print("num_ctx_switches:", process.num_ctx_switches())
    print("nice/priority get:", process.nice())

    # Error: OSError: [WinError 87] The parameter is incorrect
    # print('nice/priority set:', process.nice(10))

    # If Win and Linux
    # Error: AttributeError: module 'psutil' has no attribute 'IOPRIO_CLASS_IDLE'
    # print('ionice set:', process.ionice(psutil.IOPRIO_CLASS_IDLE))

    print("ionice get:", process.ionice())

    # If Linux
    # print('rlimit set:', process.rlimit(psutil.RLIMIT_NOFILE, (5, 5)))
    # print('rlimit get:', process.rlimit(psutil.RLIMIT_NOFILE))

    # If Linux, OSX and Windows
    print("environ:", process.environ())


if __name__ == "__main__":
    print("Random process info")

    process_pid_list = psutil.pids()

    import random
    pid = random.choice(process_pid_list)
    print("Pid:", pid)

    print_info(pid)
