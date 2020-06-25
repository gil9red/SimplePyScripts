import os.path
from pathlib import Path

file_name = Path(os.path.expanduser("~/Desktop")).resolve() / "README_YOU_WERE_HACKED.txt"
file_name.touch(exist_ok=True)
