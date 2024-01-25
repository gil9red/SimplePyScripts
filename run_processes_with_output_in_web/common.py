#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import queue

from dataclasses import dataclass, field
from subprocess import Popen
from typing import Callable
from uuid import uuid4

# pip install command_runner
from command_runner import command_runner_threaded, command_runner


class TaskStatusEnum(enum.Enum):
    Pending = enum.auto()
    Running = enum.auto()
    Finished = enum.auto()
    Stopped = enum.auto()


@dataclass
class Task:
    command: str
    id: str = field(default_factory=lambda: uuid4().hex)
    stdout: queue.Queue | Callable = field(repr=False, default=None)
    stderr: queue.Queue | Callable = field(repr=False, default=None)
    encoding: str = "utf-8"
    status: TaskStatusEnum = TaskStatusEnum.Pending
    process: Popen = field(init=False, repr=False, default=None)
    process_return_code: int = None
    __need_stop: bool = field(init=False, repr=False, default=False)

    @property
    def process_id(self) -> int | None:
        return self.process.pid if self.process else None

    def run(self, threaded: bool = False):
        self.status = TaskStatusEnum.Running

        def process_callback(process: Popen):
            self.process = process

        def on_exit():
            self.status = TaskStatusEnum.Stopped if self.__need_stop else TaskStatusEnum.Finished
            self.process_return_code = self.process.returncode

        def stop_on() -> bool:
            return self.__need_stop

        runner = command_runner_threaded if threaded else command_runner
        runner(
            self.command,
            method="poller",
            encoding=self.encoding,
            stdout=self.stdout,
            stderr=self.stderr,
            process_callback=process_callback,
            on_exit=on_exit,
            stop_on=stop_on,
        )

    def stop(self):
        self.__need_stop = True


if __name__ == "__main__":

    def process_stdout(text):
        print("process_stdout:", repr(text))

    def process_stderr(text):
        print("process_stderr:", repr(text))

    task = Task(
        command="ping 127.0.0.1",
        stdout=lambda text: process_stdout(f"[{task.command}]: {text}"),
        stderr=lambda text: process_stderr(f"[{task.command}]: {text}"),
        encoding="cp866",
    )
    print(task)
    task.run(threaded=False)
    print(task)

    print()

    stdout_queue = queue.Queue()
    stderr_queue = queue.Queue()

    task_threaded = Task(
        command=task.command,
        stdout=stdout_queue,
        stderr=stderr_queue,
        encoding=task.encoding,
    )
    print(task_threaded)

    task_threaded.run(threaded=True)
    print(task_threaded)

    while True:
        try:
            stdout_line = stdout_queue.get(timeout=0.1)
        except queue.Empty:
            stdout_line = None
        else:
            if stdout_line is not None:
                process_stdout(stdout_line)

        try:
            stderr_line = stderr_queue.get(timeout=0.1)
        except queue.Empty:
            stderr_line = None
        else:
            if stderr_line is not None:
                process_stderr(stderr_line)

        if task_threaded.status == TaskStatusEnum.Finished and not stdout_line and not stderr_line:
            break

    print()

    import threading
    threading.Timer(2, lambda: task_max_2_secs.stop()).start()
    task_max_2_secs = Task(
        command="ping 127.0.0.1",
        stdout=lambda text: process_stdout(f"[{task.command}]: {text}"),
        stderr=lambda text: process_stderr(f"[{task.command}]: {text}"),
        encoding="cp866",
    )
    print(task_max_2_secs)
    task_max_2_secs.run(threaded=False)
    print(task_max_2_secs)