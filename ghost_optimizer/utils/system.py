import platform
import os
import ctypes
import subprocess
from dataclasses import dataclass

@dataclass
class SystemInfo:
    os_name: str
    os_version: str
    is_admin: bool
    cpu_name: str
    gpu_name: str

def check_admin() -> bool:
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        return os.getuid() == 0
    except Exception:
        return False

def get_system_info() -> SystemInfo:
    cpu_name = "Unknown CPU"
    gpu_name = "Unknown GPU"

    if os.name == 'nt':
        try:
            cpu_raw = subprocess.check_output("wmic cpu get name", shell=True, text=True, errors="ignore")
            lines = [line.strip() for line in cpu_raw.split('\n') if line.strip()]
            if len(lines) > 1:
                cpu_name = lines[1]

            gpu_raw = subprocess.check_output("wmic path win32_VideoController get name", shell=True, text=True, errors="ignore")
            lines = [line.strip() for line in gpu_raw.split('\n') if line.strip()]
            if len(lines) > 1:
                gpu_name = lines[1]
        except Exception:
            pass

    return SystemInfo(
        os_name=platform.system(),
        os_version=platform.release(),
        is_admin=check_admin(),
        cpu_name=cpu_name,
        gpu_name=gpu_name
    )
