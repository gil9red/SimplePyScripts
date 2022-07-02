import psutil
# https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/


def is_running(provided_process_name: str) -> bool:
    """
    Takes the name of a process and
    returns True if it is running,
    False if it isn't"""
    for process in psutil.process_iter():
        if provided_process_name.lower() == process.name().lower():
            return True
    return False


def get_pid(provided_process_name: str) -> int:
    """
    Takes the name of a process and
    returns the process id if it
    is running"""
    for process in psutil.process_iter():
        if provided_process_name.lower() == process.name().lower():
            return process.pid
    return "Process not found"


def get_process_run_time(provided_process_name: str):
    """
    Takes the name of a process and
    returns the process runtime"""
    from datetime import datetime
    for process in psutil.process_iter():
        if provided_process_name.lower() == process.name().lower():
            epoch_created_time = process.create_time()
            dt_created_time = datetime.fromtimestamp(epoch_created_time)
            time_elapsed = datetime.now() - dt_created_time
            # https://stackoverflow.com/a/10981895
            hours, remainder = divmod(time_elapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if time_elapsed.days != 0:
                return f"{time_elapsed.days} day/s {hours} hour/s {minutes}minute/s"
            else:
                return f"{hours} hour/s {minutes} minute/s"
    return "Process not found"
