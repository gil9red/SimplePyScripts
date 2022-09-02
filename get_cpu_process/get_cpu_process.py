import psutil
import datetime as DT

# SOURCE: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/

# pip install psutil


def is_running(provided_process_name: str) -> bool:
    """
    Takes the name of a process and
    returns True if it is running,
    False if it isn't
    """
    for process in psutil.process_iter():
        if provided_process_name.lower() == process.name().lower():
            return True
    return False


def get_pid(provided_process_name: str) -> int:
    """
    Takes the name of a process and
    returns the process id if it
    is running
    """
    for process in psutil.process_iter():
        if provided_process_name.lower() == process.name().lower():
            return process.pid
    return "Process not found"


def get_process_run_time(provided_process_name: str) -> str:
    """
    Takes the name of a process and
    returns the process runtime
    """
    for process in psutil.process_iter():
        if provided_process_name.lower() == process.name().lower():
            epoch_created_time = process.create_time()
            dt_created_time = DT.datetime.fromtimestamp(epoch_created_time)
            time_elapsed = DT.datetime.now() - dt_created_time
            return str(time_elapsed).rsplit('.')[0]
    return "Process not found"
