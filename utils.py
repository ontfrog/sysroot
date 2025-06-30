import subprocess
from typing import Union

def run_cmd(cmd: Union[str, list]):
    """Run shell command with better handling of complex commands"""
    if isinstance(cmd, str):
        cmd = cmd.split()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False
    )
    return result
