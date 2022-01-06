#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.windxp.com.ru/autrun.htm
# SOURCE: http://www.infosecurity.ru/_gazeta/content/090904/art3.shtml
# SOURCE: https://www.saule-spb.ru/library/autorun.html


from typing import Dict, List

from common import expand_path, get_key, Entry, get_entries, get_entry


PATHS = [
    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKCU\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",
    r"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",

    r"HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKCU\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",

    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",

    r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"HKCU\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",

    r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Runonce",
    r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunonceEx",

    r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Runonce",
    r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunonceEx",

    (r"HKLM\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp", "InitialProgram"),
    (r"HKLM\System\CurrentControlSet\Control\Terminal Server\Wds\rdpwd", "StartupPrograms"),

    r"HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup",

    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Windows", "IconServiceLib"),

    (r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows", "Load"),
    (r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows", "Run"),

    (r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Shell"),

    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "AppSetup"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Shell"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Taskman"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Userinit"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "VmApplet"),
    r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells\AvailableShells",

    (r"HKLM\SYSTEM\CurrentControlSet\Control\SafeBoot", "AlternateShell"),

    (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System", "Shell"),
    (r"HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System", "Shell"),

    (r"HKCU\Environment", "UserInitMprLogonScript"),
    (r"HKLM\Environment", "UserInitMprLogonScript"),

    r"HKLM\Software\Microsoft\Windows CE Services\AutoStartOnConnect",
    r"HKLM\Software\Microsoft\Windows CE Services\AutoStartOnDisconnect",

    r"HKLM\Software\Wow6432Node\Microsoft\Windows CE Services\AutoStartOnConnect",
    r"HKLM\Software\Wow6432Node\Microsoft\Windows CE Services\AutoStartOnDisconnect",
]

# SOURCE: https://www.microsoftpressstore.com/articles/article.aspx?p=2762082&seqNum=2
r"""
# Per-user ASEPs under HKCU\Software intended to be controlled through Group Policy
HKCU\Software\Policies\Microsoft\Windows\System\Scripts\Logon
HKCU\Software\Policies\Microsoft\Windows\System\Scripts\Logoff

# Systemwide ASEPs in the registry, intended to be controlled through Group Policy
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Logon
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Logoff
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Startup
HKLM\Software\Policies\Microsoft\Windows\System\Scripts\Shutdown
HKLM\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Startup
HKLM\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Shutdown
"""


def get_run_paths(expand_vars=True) -> Dict[str, List[Entry]]:
    path_by_entries = dict()

    for path in PATHS:
        if isinstance(path, str):
            path = expand_path(path)
            key = get_key(path)
            if not key:
                continue

            path_by_entries[path] = get_entries(path, expand_vars)

        elif isinstance(path, tuple):
            path, name = path
            path = expand_path(path)
            entry = get_entry(path, name)
            if entry:
                if path not in path_by_entries:
                    path_by_entries[path] = []

                path_by_entries[path].append(entry)

    return path_by_entries


if __name__ == '__main__':
    run_paths = get_run_paths()
    for path, entries in run_paths.items():
        if not entries:
            continue

        print(path)

        for i, entry in enumerate(entries, 1):
            print(f'    {i}. {entry.name}: {entry.value}')

        print()
    r"""
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
        1. Lync: "C:\Program Files (x86)\Microsoft Office\Office15\lync.exe" /fromrunkey
        2. Zoom: "C:\Users\IPetrash\AppData\Roaming\Zoom\bin\Zoom.exe"
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
        1. RTHDVCPL: "C:\Program Files\Realtek\Audio\HDA\RtkNGUI64.exe" -s
        2. DocFetcher-Daemon: C:\Program Files (x86)\DocFetcher\docfetcher-daemon-windows.exe
        3. egui: "C:\Program Files\ESET\ESET Security\ecmds.exe" /run /hide /proxy
        4. SecurityHealth: C:\Program Files\Windows Defender\MSASCuiL.exe
    
    HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run
        1. Dropbox: "C:\Program Files (x86)\Dropbox\Client\Dropbox.exe" /systemstartup
        2. SystemExplorerAutoStart: "C:\Program Files (x86)\System Explorer\SystemExplorer.exe" /TRAY
        3. Zet Warrior: "C:\Program Files (x86)\Zet Warrior\Monitor.exe"

    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon
        1. Shell: explorer.exe
        2. Userinit: C:\Windows\system32\userinit.exe,
    
    HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SafeBoot
        1. AlternateShell: cmd.exe
    
    """