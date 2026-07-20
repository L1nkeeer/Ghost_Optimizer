import os
import logging

logger = logging.getLogger("GhostOptimizer")

try:
    import winreg
except ImportError:
    winreg = None

def set_reg_key(hkey, subkey: str, value_name: str, value_data, value_type=None) -> bool:
    if not winreg:
        return False
    try:
        if value_type is None:
            if isinstance(value_data, int):
                value_type = winreg.REG_DWORD
            else:
                value_type = winreg.REG_SZ

        with winreg.CreateKeyEx(hkey, subkey, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        return True
    except Exception as e:
        logger.error(f"Failed to set registry key {subkey}\\{value_name}: {e}")
        return False

def delete_reg_key(hkey, subkey: str, value_name: str) -> bool:
    if not winreg:
        return False
    try:
        with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, value_name)
        return True
    except FileNotFoundError:
        return True # Already deleted
    except Exception as e:
        logger.error(f"Failed to delete registry key {subkey}\\{value_name}: {e}")
        return False
