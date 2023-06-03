#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import subprocess

from pymem import Pymem


# TODO: user
# 2021-02-05 13:17:35,762 - pymem - DEBUG - Process 48824 is being debugged
# 2021-02-05 13:17:35,787 - pymem - WARNING - Got an error in start thread, code: 87
# 2021-02-05 13:17:35,799 - pymem - DEBUG - New thread_id: 0x000001d0
# 2021-02-05 13:17:35,799 - pymem - DEBUG - Py_InitializeEx loc: 0x7ff853a31e08
# 2021-02-05 13:17:35,799 - pymem - DEBUG - PyRun_SimpleString loc: 0x7ff853a45348
# 2021-02-05 13:17:35,799 - pymem - DEBUG - shellcode_addr loc: 0x2358be30000
# 2021-02-05 13:17:35,799 - pymem - WARNING - Got an error in start thread, code: 5
# Traceback (most recent call last):
#   File "C:/Users/ipetrash/Projects/SimplePyScripts/pymem__examples/inject_python_interpreter.py", line 22, in <module>
#     pm.inject_python_shellcode(shellcode)
#   File "C:\Users\ipetrash\Anaconda3\lib\site-packages\pymem\__init__.py", line 147, in inject_python_shellcode
#     self.start_thread(self.py_run_simple_string, shellcode_addr)
#   File "C:\Users\ipetrash\Anaconda3\lib\site-packages\pymem\__init__.py", line 180, in start_thread
#     pymem.logger.debug('New thread_id: 0x%08x' % thread_h)
# TypeError: %x format: an integer is required, not NoneType
#
# Process finished with exit code 1

# TODO: admin
# 2021-02-05 13:18:14,957 - pymem - DEBUG - Process 20412 is being debugged
# 2021-02-05 13:18:14,977 - pymem - WARNING - Got an error in start thread, code: 87
# 2021-02-05 13:18:14,995 - pymem - DEBUG - New thread_id: 0x00000234
# 2021-02-05 13:18:14,995 - pymem - DEBUG - Py_InitializeEx loc: 0x7ff853a31e08
# 2021-02-05 13:18:14,995 - pymem - DEBUG - PyRun_SimpleString loc: 0x7ff853a45348
# Traceback (most recent call last):
#   File "C:\Users\ipetrash\Projects\SimplePyScripts\pymem__examples\inject_python_interpreter.py", line 22, in <module>
#     pm.inject_python_shellcode(shellcode)
#   File "C:\Users\ipetrash\Anaconda3\lib\site-packages\pymem\__init__.py", line 142, in inject_python_shellcode
#     raise RuntimeError('Could not allocate memory for shellcode')
# RuntimeError: Could not allocate memory for shellcode


notepad = subprocess.Popen(["notepad.exe"])

pm = Pymem("notepad.exe")
pm.inject_python_interpreter()
filepath = os.path.join(os.path.abspath("."), "pymem_injection.txt")
filepath = filepath.replace("\\", "\\\\")
shellcode = """
f = open("{}", "w+")
f.write("pymem_injection")
f.close()
""".format(
    filepath
)
pm.inject_python_shellcode(shellcode)
notepad.kill()
