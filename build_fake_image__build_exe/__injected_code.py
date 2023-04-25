import os.path
from pathlib import Path


DIR = Path(os.path.expanduser("~/Desktop")).resolve()
file_name = DIR / "README_YOU_WERE_HACKED.txt"
file_name.touch(exist_ok=True)
