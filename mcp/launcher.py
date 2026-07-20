import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
VENV = HERE / ".venv"
PYTHON = VENV / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python3")


def _bootstrap():
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV)])
    subprocess.check_call([
        str(PYTHON), "-m", "pip", "install", "-q",
        "-r", str(HERE / "requirements.txt"),
    ])


if not PYTHON.exists():
    _bootstrap()

os.execv(str(PYTHON), [str(PYTHON), str(HERE / "server.py")])
