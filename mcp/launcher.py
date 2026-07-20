import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
VENV = HERE / ".venv"
PYTHON = VENV / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python3")
REQUIREMENTS = HERE / "requirements.txt"


def _bootstrap():
    if shutil.which("uv"):
        subprocess.check_call([
            "uv", "venv", str(VENV), "--python", sys.executable,
        ])
        subprocess.check_call([
            "uv", "pip", "install", "--python", str(PYTHON),
            "-q", "-r", str(REQUIREMENTS),
        ])
    else:
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV)])
        subprocess.check_call([
            str(PYTHON), "-m", "pip", "install", "-q", "-r", str(REQUIREMENTS),
        ])


if not PYTHON.exists():
    _bootstrap()

os.execv(str(PYTHON), [str(PYTHON), str(HERE / "server.py")])
