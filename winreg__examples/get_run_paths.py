#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.windxp.com.ru/autrun.htm
# SOURCE: http://www.infosecurity.ru/_gazeta/content/090904/art3.shtml
# SOURCE: https://www.saule-spb.ru/library/autorun.html


from collections import defaultdict
from common import RegistryKey


PATHS = [
    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKCU\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",
    r"HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",

    r"HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKCU\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",

    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",

    r"HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"HKCU\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",

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
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "GinaDLL"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Shell"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "System"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Taskman"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "UIHost"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "Userinit"),
    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "VMApplet"),
    r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells\AvailableShells",

    (r"HKLM\SYSTEM\CurrentControlSet\Control\SafeBoot", "AlternateShell"),
    (r"HKLM\SYSTEM\CurrentControlSet\Control\BootVerificationProgram", "ImageName"),

    (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System", "Shell"),
    (r"HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System", "Shell"),

    (r"HKCU\Environment", "UserInitMprLogonScript"),
    (r"HKLM\Environment", "UserInitMprLogonScript"),

    r"HKLM\Software\Microsoft\Windows CE Services\AutoStartOnConnect",
    r"HKLM\Software\Microsoft\Windows CE Services\AutoStartOnDisconnect",

    r"HKLM\Software\Wow6432Node\Microsoft\Windows CE Services\AutoStartOnConnect",
    r"HKLM\Software\Wow6432Node\Microsoft\Windows CE Services\AutoStartOnDisconnect",

    (r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Windows", "AppInit_DLLs"),
    (r"HKLM\Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Windows", "AppInit_DLLs"),

    (r"HKCU\Control Panel\Desktop", "SCRNSAVE.EXE"),
    (r"HKLM\SYSTEM\Setup", "CmdLine"),
]


def get_key_by_values() -> dict[str, dict[str, str]]:
    path_by_values = defaultdict(dict)

    for path in PATHS:
        if isinstance(path, tuple):
            path, name = path
        else:
            name = None

        key = RegistryKey.get_or_none(path)
        if not key:
            continue

        path = key.path

        if name:
            if value := key.get_str_value(name):
                path_by_values[path][name] = value
        else:
            path_by_values[path].update(key.get_str_values_as_dict())

    return path_by_values


def get_run_paths() -> dict[str, str]:
    run_paths = dict()
    for path, name_by_value in get_key_by_values().items():
        for name, value in name_by_value.items():
            run_paths[f"{path}, {name}"] = value

    return run_paths


if __name__ == "__main__":
    for path, name_by_value in get_key_by_values().items():
        if not name_by_value:
            continue

        print(path)

        for i, (name, value) in enumerate(name_by_value.items(), 1):
            print(f"    {i}. {name}: {value}")

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

    run_paths = get_run_paths()
    print(len(run_paths), run_paths)
